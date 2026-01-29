from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    base_url: str = Field(
        default="https://cloud-api.yandex.net", description="The base URL Yandex_API."
    )
    yandex_token: str = Field(default="", description="Your Yandex API Token.")

    yandex_login: str = Field(default="", description="Your Yandex login.")
    yandex_display_name: str = Field(default="", description="Your Yandex displayname.")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )


settings = Config()
