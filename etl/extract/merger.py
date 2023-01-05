from typing import Any
from typing import Generator

import psycopg2
from psycopg2.extensions import cursor
from utils.logger import logger


class PostgresMerger:
    def get_filmworks_data(
        self,
        curs: cursor,
        upload_filmwork_data_batch: int,
        filmwork_ids_statement: str,
    ) -> Generator[Any, None, None]:

        try:
            curs.execute(
                f"""
                SELECT
                fw.id as fw_id,
                fw.title,
                fw.description,
                fw.rating,
                fw.type,
                fw.created_at,
                fw.updated_at,
                pfw.role,
                p.id,
                p.full_name,
                g.name
                FROM content.film_work fw
                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                LEFT JOIN content.person p ON p.id = pfw.person_id
                LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                LEFT JOIN content.genre g ON g.id = gfw.genre_id
                WHERE fw.id IN {filmwork_ids_statement};
                """
            )
            while rows_data := curs.fetchmany(upload_filmwork_data_batch):
                yield rows_data

        except psycopg2.Error as error:
            logger.error("Failed to get filmworks data", error)
