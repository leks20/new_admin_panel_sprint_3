import json
from typing import Any

import requests
from config import settings
from utils.backoff import backoff

ELACTIC_INDEX_SCHEMA = {
    "settings": {
        "refresh_interval": "1s",
        "analysis": {
            "filter": {
                "english_stop": {"type": "stop", "stopwords": "_english_"},
                "english_stemmer": {"type": "stemmer", "language": "english"},
                "english_possessive_stemmer": {
                    "type": "stemmer",
                    "language": "possessive_english",
                },
                "russian_stop": {"type": "stop", "stopwords": "_russian_"},
                "russian_stemmer": {"type": "stemmer", "language": "russian"},
            },
            "analyzer": {
                "ru_en": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_possessive_stemmer",
                        "russian_stop",
                        "russian_stemmer",
                    ],
                }
            },
        },
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {"type": "keyword"},
            "imdb_rating": {"type": "float"},
            "genre": {"type": "keyword"},
            "title": {
                "type": "text",
                "analyzer": "ru_en",
                "fields": {"raw": {"type": "keyword"}},
            },
            "description": {"type": "text", "analyzer": "ru_en"},
            "director": {"type": "text", "analyzer": "ru_en"},
            "actors_names": {"type": "text", "analyzer": "ru_en"},
            "writers_names": {"type": "text", "analyzer": "ru_en"},
            "actors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {"type": "text", "analyzer": "ru_en"},
                },
            },
            "writers": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {"type": "text", "analyzer": "ru_en"},
                },
            },
        },
    },
}


class ElasticSearch:
    @backoff
    def create_index(self) -> None:

        json_index_schema = json.dumps(ELACTIC_INDEX_SCHEMA)

        url = f"{settings.ELASTIC_HOST}/movies"
        requests.put(
            url,
            headers={"Content-Type": "application/x-ndjson"},
            data=json_index_schema,
        )

    @backoff
    def load_data(self, data_for_elasticsearch: dict[str, Any]) -> None:

        url = f"{settings.ELASTIC_HOST}/_bulk"

        bulk_data = ""

        for data in data_for_elasticsearch.values():
            bulk_data += f"""{{"index": {{"_index": "movies", "_id": "{data['id']}"}}}}\n{json.dumps(data)}\n"""

        requests.post(
            url,
            headers={"Content-Type": "application/x-ndjson", "charset": "UTF-8"},
            data=bulk_data,
        )
