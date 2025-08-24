from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "EuroDisney API"
    database_url: str = "mysql+pymysql://root:supersaiyan@localhost/eurodisney?charset=utf8mb4"
    secret_key: str = "mykey"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    BACKEND_CORS_ORIGINS: str = "*"

    class Config:
        env_file = ".env.backend"
    
settings = Settings()