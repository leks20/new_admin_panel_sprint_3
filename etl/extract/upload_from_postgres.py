from datetime import datetime
from typing import Any
from typing import Generator

from config import settings
from extract.enricher import PostgresEnricher
from extract.merger import PostgresMerger
from extract.producer import PostgresProducer
from psycopg2.extensions import connection as pg_connection
from utils.state import start_state


class PostgresExtractor(
    PostgresProducer,
    PostgresEnricher,
    PostgresMerger,
):
    def __init__(self, connection: pg_connection) -> None:
        self.connection = connection
        self.curs = self.connection.cursor()
        self.connection.autocommit = False
        self.upload_persons_batch = settings.UPLOAD_PERSON_ID_BATCH
        self.upload_filmworks_batch = settings.UPLOAD_FILMWORK_ID_BATCH
        self.upload_filmwork_data_batch = settings.UPLOAD_FILMWORK_DATA_BATCH
        self.state = start_state()

    def change_state(
        self,
        modified: datetime,
        person_ids_statement: str | None = None,
        genre_ids_statement: str | None = None,
        filmwork_ids_statement: str | None = None,
    ) -> None:

        if person_ids_statement:
            state_unit = "person_modified"

        elif genre_ids_statement:
            state_unit = "genre_modified"

        elif filmwork_ids_statement:
            state_unit = "filmwork_modified"

        self.connection.commit()
        self.state.set_state(state_unit, modified)

    def get_data_from_generator(
        self, data_generator: Generator[Any, None, None], result: list[str]
    ) -> tuple[list[str], datetime]:

        modified = datetime.min

        for data in data_generator:
            result.extend(data[0])
            modified = data[1]

        return result, modified

    def upload_from_postgres(self) -> list[Any]:
        """
        Return Postgres data
        """
        all_person_ids: list[str] = []
        all_genre_ids: list[str] = []
        all_filmwork_ids: list[str] = []
        filmwork_data: list[Any] = []

        # Get pesons ids
        person_data_generator = self.get_persons_ids(
            self.curs,
            self.upload_persons_batch,
            self.state,
        )
        all_person_ids, modified = self.get_data_from_generator(
            person_data_generator, all_person_ids
        )

        if all_person_ids:
            person_ids_statement = f"({str(all_person_ids)[1:-1]})"
            self.change_state(modified, person_ids_statement=person_ids_statement)

        # Get genre ids
        genre_data_generator = self.get_genre_ids(self.curs, self.state)

        all_genre_ids, modified = self.get_data_from_generator(
            genre_data_generator, all_genre_ids
        )

        if all_genre_ids:
            genre_ids_statement = f"({str(all_genre_ids)[1:-1]})"
            self.change_state(modified, genre_ids_statement=genre_ids_statement)

        # Get filmworks ids
        if all_person_ids:
            film_data_generator = self.get_filmworks_ids(
                curs=self.curs,
                state=self.state,
                upload_filmworks_batch=self.upload_filmworks_batch,
                person_ids_statement=person_ids_statement,
            )

            all_filmwork_ids, modified = self.get_data_from_generator(
                film_data_generator, all_filmwork_ids
            )

        if all_genre_ids:
            film_data_generator = self.get_filmworks_ids(
                curs=self.curs,
                state=self.state,
                upload_filmworks_batch=self.upload_filmworks_batch,
                genre_ids_statement=genre_ids_statement,
            )

            all_filmwork_ids, modified = self.get_data_from_generator(
                film_data_generator, all_filmwork_ids
            )

        film_data_generator = self.get_filmworks_ids(
            curs=self.curs,
            state=self.state,
            upload_filmworks_batch=self.upload_filmworks_batch,
            with_no_persons_and_genres=True,
        )

        all_filmwork_ids, modified = self.get_data_from_generator(
            film_data_generator, all_filmwork_ids
        )

        if all_filmwork_ids:
            filmwork_ids_statement = f"({str(all_filmwork_ids)[1:-1]})"
            self.change_state(modified, filmwork_ids_statement=filmwork_ids_statement)

        # Get filmwork data
        if all_filmwork_ids:
            filmwork_data_generator = self.get_filmworks_data(
                self.curs,
                self.upload_filmwork_data_batch,
                filmwork_ids_statement,
            )

            for filmwork_data_batch in filmwork_data_generator:
                for fdb in filmwork_data_batch:
                    if fdb not in filmwork_data:
                        filmwork_data.append(fdb)

        return filmwork_data
