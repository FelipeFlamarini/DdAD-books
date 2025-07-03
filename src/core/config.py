from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import Optional


class __Settings__(BaseSettings):
    model_config = SettingsConfigDict()

    mongo_uri: str = "mongodb://root:changeme@db-test:27017"
    mongo_db_name: Optional[str] = "my-db"

    rabbitmq_url: Optional[str] = ""

    mailgun_api_key: Optional[str] = ""
    mailgun_domain: Optional[str] = ""
    mailgun_sender: Optional[str] = ""

    company_name: Optional[str] = "My Company"
    support_email: Optional[str] = "support@example.com"


@lru_cache
def get_settings() -> __Settings__:
    return __Settings__()
