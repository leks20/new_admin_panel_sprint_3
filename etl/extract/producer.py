from datetime import datetime
from typing import Generator

import psycopg2
from psycopg2.extensions import cursor
from utils.logger import logger
from utils.state import State


class PostgresProducer:
    def get_persons_ids(
        self,
        curs: cursor,
        upload_persons_batch: int,
        state: State,
    ) -> Generator[tuple[list[str], datetime], None, None]:

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
                modified = rows_data[-1][-1]
                yield [row[0] for row in rows_data], modified

        except psycopg2.Error as error:
            logger.error("Failed to get persons data", error)

    def get_genre_ids(
        self,
        curs: cursor,
        state: State,
    ) -> Generator[tuple[list[str], datetime], None, None]:

        try:
            modified = state.get_state("genre_modified")

            curs.execute(
                f"""
                SELECT id, updated_at
                FROM content.genre
                WHERE updated_at > '{modified}'
                ORDER BY updated_at
                """
            )

            while rows_data := curs.fetchall():
                modified = rows_data[-1][-1]
                yield [row[0] for row in rows_data], modified

        except psycopg2.Error as error:
            logger.error("Failed to get genres data", error)
