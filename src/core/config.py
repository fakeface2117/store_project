import orjson
from pydantic import BaseSettings
from pydantic.main import BaseModel


class Settings(BaseSettings):
    POSTGRES_USER: str = "app"
    POSTGRES_PASS: str = "123qwe"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "orders_database"
    DRIVER: str = "postgresql+asyncpg"
    CONNECTION_STRING: str = f"{DRIVER}://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str = "something_secret_key"
    ALGORITHM_HASH: str = "HS256"

    class Config:
        env_prefix = "API_STORE_"
        env_file = ".env"
        case_sensitive = False

settings = Settings()

def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Base(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
