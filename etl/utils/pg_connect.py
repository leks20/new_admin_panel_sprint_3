import time
from contextlib import contextmanager
from typing import Any
from typing import Generator

import psycopg2
from config import settings
from psycopg2.extras import DictCursor
from utils.logger import logger


@contextmanager
def pg_conn_context_with_backoff(
    sleep_time: float = 0.1, factor: int = 2, border_sleep_time: int = 10
) -> Generator[Any, None, None]:

    dsn = {
        "dbname": settings.POSTGRES_DB,
        "user": settings.POSTGRES_USER,
        "password": settings.POSTGRES_PASSWORD,
        "host": settings.POSTGRES_SERVER,
        "port": settings.POSTGRES_PORT,
    }

    try:
        while True:
            try:
                conn = psycopg2.connect(**dsn, cursor_factory=DictCursor)
                logger.info("Successful connection with Postgres")
                yield conn
            except psycopg2.OperationalError:
                if (sleep_time := sleep_time * (2**factor)) >= border_sleep_time:
                    sleep_time = border_sleep_time
                logger.error("Unable to connect with Postgres")
                time.sleep(sleep_time)
            else:
                break
    finally:
        conn.close()
