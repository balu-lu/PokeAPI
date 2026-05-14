from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    PROJECT_NAME: str = "Pokedex API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # PokeAPI
    POKEAPI_BASE_URL: str = "https://pokeapi.co/api/v2"

    # Redis Cache
    # URL padrão para rodar localmente no Docker
    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TTL: int = 3600  # 1 hora


settings = Settings()
