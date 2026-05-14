from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Pokedex API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # PokeAPI
    POKEAPI_BASE_URL: str = "https://pokeapi.co/api/v2"

    # Redis Cache
    REDIS_HOST: str = "localhost"  # Será sobrescrito no Docker
    REDIS_PORT: int = 6379
    CACHE_TTL: int = 3600  # 1 hora

    class Config:
        env_file = ".env"


settings = Settings()
