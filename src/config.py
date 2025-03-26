from pathlib import Path

# from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_PATH = Path(__file__).parent.parent

"""
The class Settings will attempt to determine the values of any fields not passed as keyword arguments by reading either
from the environment or a .env file in the service_guide_design folder.
(Default values will still be used if the matching environment variable is not set.)
"""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_PATH / ".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    # Application Configuration
    SERVICE_NAME: str = "Structure Logging"
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    ORIGINS: list = [
        "http://localhost",
        f"http://localhost:{PORT}",
    ]

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_SAVE_ON_FILE: bool = False

    # Authentication and Authorization
    # API_KEY: SecretStr


settings = Settings()  # type: ignore


def init_whatever():
    # Initialise whatever
    ...
