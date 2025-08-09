from pathlib import Path
from typing import Optional, Any

from decouple import config as decouple_conf
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, field_validator, ValidationInfo

class Settings(BaseSettings):
    PROJECT_NAME: str = "LEAFLOG"
    SECRET_KEY: str = decouple_conf("SECRET_KEY")
    PROTECTED_API_KEY: str = decouple_conf("PROTECTED_API_KEY")
    ROOT_URL_PREFIX: str = f"/{PROJECT_NAME.lower()}"

    BASE_DIR: str = str(Path(__file__).resolve().parent.parent.parent)
    IS_DEV: bool = decouple_conf('IS_DEV', cast=bool, default=False)

    DATABASE_USER: str = decouple_conf('DATABASE_USER')
    DATABASE_PASSWORD: str = decouple_conf('DATABASE_PASSWORD')
    DATABASE_HOST: str = decouple_conf('DATABASE_HOST')
    DATABASE_PORT: int = decouple_conf('DATABASE_PORT')
    DATABASE_NAME: str = decouple_conf('DATABASE_NAME')
    SQL_DATABASE_URI: Optional[PostgresDsn] = None

    ACCESS_TOKEN_EXPIRE_MINUTES: int = decouple_conf('ACCESS_TOKEN_EXPIRE_MINUTES')
    REFRESH_TOKEN_EXPIRE_MINUTES: int = decouple_conf('REFRESH_TOKEN_EXPIRE_MINUTES')

    SMTP_SERVER: str = decouple_conf('SMTP_SERVER')
    SMTP_PORT:int = decouple_conf('SMTP_PORT', 587)
    SMTP_USERNAME: str = decouple_conf('SMTP_USERNAME')
    SMTP_PASSWORD: str = decouple_conf('SMTP_PASSWORD')
    FROM_MAIL: str = decouple_conf('FROM_MAIL')

    @field_validator("SQL_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.data.get("DATABASE_USER"),
            password=values.data.get("DATABASE_PASSWORD"),
            host=values.data.get("DATABASE_HOST"),
            path=values.data.get('DATABASE_NAME'),
            port=values.data.get('DATABASE_PORT')
        )


settings = Settings()