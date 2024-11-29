import os


class Settings:
    PROJECT_NAME: str = "apptivity"
    PROJECT_DESCRIPTION: str = "API to manage apptivity"
    PROJECT_VERSION: str = "0.1.0"

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
