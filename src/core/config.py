from decouple import config
from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    LOG_LEVEL: str =config('LOG_LEVEL')


    MONGO_HOST: str = config('MONGO_HOST')
    MONGO_PORT: str = config('MONGO_PORT')
    MONGO_DATABASE: str = config('MONGO_DATABASE')
    MONGO_USER: str = config('MONGO_USER')
    MONGO_PASSWORD: str = config('MONGO_PASSWORD')

    class Config:
        env_file = ".env"

settings = Setting()