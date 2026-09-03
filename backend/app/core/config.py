import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "EuroDisney API"

    database_url: str = (
        "mysql+pymysql://root@localhost:3306/eurodisney?charset=utf8mb4"
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

    @property
    def effective_database_url(self) -> str:
        if os.getenv("VERCEL"):
            if os.name == "nt":
                # Simulation Vercel sous Windows
                return "sqlite:///./eurodisney_vercel.db"

            # Vercel fonctionne sous Linux et /tmp est inscriptible
            return "sqlite:////tmp/eurodisney.db"

        return self.database_url
    
settings = Settings()