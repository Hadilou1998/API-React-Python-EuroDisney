from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "EuroDisney API"

    database_url: str = (
        "mysql+pymysql://root@localhost/eurodisney?charset=utf8mb4"
    )

    secret_key: str = "mykey"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    BACKEND_CORS_ORIGINS: str = "*"

    model_config = SettingsConfigDict(
        env_file=".env.backend",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
settings = Settings()