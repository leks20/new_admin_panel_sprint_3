import logging
from typing import Generator

import psycopg2
from psycopg2.extensions import cursor
from utils.state import State

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class PostgresProducer:
    def get_persons_ids(
        self,
        curs: cursor,
        upload_persons_batch: int,
        state: State,
    ) -> Generator[list[str], None, None]:

        try:
            modified = state.get_state("person_modified")

            curs.execute(
                f"""
                SELECT id, updated_at
                FROM content.person
                WHERE updated_at > '{modified}'
                ORDER BY updated_at
                """
            )

            while rows_data := curs.fetchmany(upload_persons_batch):
                yield [row[0] for row in rows_data]

        except psycopg2.Error as error:
            logger.error("Failed to get persons data", error)
