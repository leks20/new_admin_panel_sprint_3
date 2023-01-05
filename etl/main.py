import time

from extract.upload_from_postgres import PostgresExtractor
from load.elastic import ElasticSearch
from transform.transform import DataTransformer
from utils.logger import logger
from utils.pg_connect import pg_conn_context_with_backoff


def start_etl_proccess() -> None:
    """Метод для переноса данных из Postgres в ElasticSerach"""

    # Extract data
    with pg_conn_context_with_backoff() as pg_conn:
        postgres_extractor = PostgresExtractor(pg_conn)
        filmwork_data = postgres_extractor.upload_from_postgres()

    if not filmwork_data:
        logger.info("No data changed")
        return None

    logger.info(f"Recieved data. Count: {len(filmwork_data)}")

    # Transform data
    transformer = DataTransformer()
    data_for_elasticsearch = transformer.transform_data(filmwork_data)

    logger.info(f"Trasformed data. Count: {len(data_for_elasticsearch)}")

    # Load data
    elactic = ElasticSearch()
    elactic.create_index()
    elactic.load_data(data_for_elasticsearch)

    logger.info("Data loaded")


if __name__ == "__main__":
    while True:
        start_etl_proccess()
        time.sleep(10)
