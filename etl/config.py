from pydantic import BaseSettings


class Settings(BaseSettings):

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432

    DJANGO_LOG_LEVEL: str = "DEBUG"

    UPLOAD_PERSON_ID_BATCH: int
    UPLOAD_FILMWORK_ID_BATCH: int
    UPLOAD_FILMWORK_DATA_BATCH: int

    ELASTIC_HOST: str

    class Config:
        env_file = "./.env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
