import logging
from typing import Any
from typing import Generator

import psycopg2
from psycopg2.extensions import cursor
from utils.state import State

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class PostgresEnricher:
    def get_filmworks_ids(
        self,
        curs: cursor,
        state: State,
        upload_filmworks_batch: int,
        person_ids_statement: str | None = None,
        with_no_persons: bool = False,
    ) -> Generator[Any, None, None]:

        try:
            modified = state.get_state("filmwork_modified")

            if with_no_persons:
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

                while rows_data := curs.fetchmany(upload_filmworks_batch):
                    yield [row[0] for row in rows_data]
            else:
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
                while rows_data := curs.fetchmany(upload_filmworks_batch):
                    yield [row[0] for row in rows_data]

        except psycopg2.Error as error:
            logger.error("Failed to get filmworks ids", error)
