import httpx
import json
import redis.asyncio as redis
from app.core.config import settings
from app.utils.exceptions import PokemonNotFoundException, ExternalAPIException

# Inicialização do cliente Redis atualizada para aceitar URL
redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True
)


async def get_pokemons(limit: int = 10, offset: int = 0) -> dict:
    cache_key = f"pokemons:limit={limit}:offset={offset}"

    # Tenta buscar no cache primeiro
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    # Se não tem no cache, busca na PokeAPI
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{settings.POKEAPI_BASE_URL}/pokemon?limit={limit}&offset={offset}")
            response.raise_for_status()
        except httpx.HTTPError:
            raise ExternalAPIException("Erro ao comunicar com a PokeAPI")

        data = response.json()

        # Formatando exatamente como o `arquivo_requirements.md` exige
        result = {
            "data": data.get("results", []),
            "pagination": {
                "total": data.get("count", 0),
                "limit": limit,
                "offset": offset,
                "next": f"/pokemons?limit={limit}&offset={offset + limit}" if data.get("next") else None,
                "previous": f"/pokemons?limit={limit}&offset={max(0, offset - limit)}" if data.get("previous") else None
            }
        }

        # Salva no cache
        await redis_client.setex(cache_key, settings.CACHE_TTL, json.dumps(result))
        return result


async def get_pokemon_by_id(pokemon_id: int) -> dict:
    cache_key = f"pokemon:{pokemon_id}"

    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.POKEAPI_BASE_URL}/pokemon/{pokemon_id}")

        if response.status_code == 404:
            raise PokemonNotFoundException(str(pokemon_id))
        elif response.status_code != 200:
            raise ExternalAPIException("Erro ao comunicar com a PokeAPI")

        data = response.json()

        # Mapeando os dados complexos para o JSON de resposta exigido
        result = {
            "id": data["id"],
            "name": data["name"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [t["type"]["name"] for t in data.get("types", [])],
            "sprites": {
                "front_default": data.get("sprites", {}).get("front_default"),
                "back_default": data.get("sprites", {}).get("back_default")
            }
        }

        await redis_client.setex(cache_key, settings.CACHE_TTL, json.dumps(result))
        return result
