from typing import Any
from typing import Generator

import psycopg2
from psycopg2.extensions import cursor
from utils.logger import logger
from utils.state import State


class PostgresEnricher:
    def get_filmworks_ids(
        self,
        curs: cursor,
        state: State,
        upload_filmworks_batch: int,
        person_ids_statement: str | None = None,
        genre_ids_statement: str | None = None,
        with_no_persons_and_genres: bool = False,
    ) -> Generator[Any, None, None]:

        try:
            modified = state.get_state("filmwork_modified")

            if with_no_persons_and_genres:
                curs.execute(
                    f"""
                    SELECT fw.id, fw.updated_at
                    FROM content.film_work fw
                    WHERE fw.id not in
                    (select pfw.film_work_id
                    FROM content.person_film_work pfw)
                    AND fw.updated_at > '{modified}'
                    ORDER BY fw.updated_at;
                    """
                )

            elif person_ids_statement:
                curs.execute(
                    f"""
                    SELECT fw.id, fw.updated_at
                    FROM content.film_work fw
                    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                    WHERE pfw.person_id IN {person_ids_statement} AND
                        fw.updated_at > '{modified}'
                    ORDER BY fw.updated_at;
                    """
                )

            elif genre_ids_statement:
                curs.execute(
                    f"""
                    SELECT fw.id, fw.updated_at
                    FROM content.film_work fw
                    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                    WHERE gfw.genre_id IN {genre_ids_statement} AND
                        fw.updated_at > '{modified}'
                    ORDER BY fw.updated_at;
                    """
                )

            while rows_data := curs.fetchmany(upload_filmworks_batch):
                modified = rows_data[-1][-1]
                yield [row[0] for row in rows_data], modified

        except psycopg2.Error as error:
            logger.error("Failed to get filmworks ids", error)
