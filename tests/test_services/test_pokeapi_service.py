import json
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.services import pokeapi_service
from app.utils.exceptions import ExternalAPIException, PokemonNotFoundException


@pytest.mark.anyio
async def test_get_pokemons_returns_cached_data():
    cached_payload = {"data": [{"name": "bulbasaur", "url": "url"}], "pagination": {"total": 1}}

    with patch.object(pokeapi_service.redis_client, "get", AsyncMock(return_value=json.dumps(cached_payload))), \
         patch.object(pokeapi_service.redis_client, "setex", AsyncMock()) as mock_setex:
        result = await pokeapi_service.get_pokemons(limit=1, offset=0)

    assert result == cached_payload
    mock_setex.assert_not_awaited()


@pytest.mark.anyio
async def test_get_pokemons_fetches_and_caches_when_cache_is_empty():
    response_payload = {
        "count": 1281,
        "next": "https://pokeapi.co/api/v2/pokemon?offset=2&limit=2",
        "previous": None,
        "results": [
            {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
            {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"},
        ],
    }
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = response_payload

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response
    mock_context_manager = AsyncMock()
    mock_context_manager.__aenter__.return_value = mock_client
    mock_context_manager.__aexit__.return_value = None

    with patch.object(pokeapi_service.redis_client, "get", AsyncMock(return_value=None)), \
         patch.object(pokeapi_service.redis_client, "setex", AsyncMock()) as mock_setex, \
         patch("app.services.pokeapi_service.httpx.AsyncClient", return_value=mock_context_manager):
        result = await pokeapi_service.get_pokemons(limit=2, offset=0)

    assert result["data"] == response_payload["results"]
    assert result["pagination"]["total"] == 1281
    assert result["pagination"]["next"] == "/pokemons?limit=2&offset=2"
    assert result["pagination"]["previous"] is None
    mock_setex.assert_awaited_once()


@pytest.mark.anyio
async def test_get_pokemon_by_id_raises_not_found_for_404():
    mock_response = MagicMock()
    mock_response.status_code = 404

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response
    mock_context_manager = AsyncMock()
    mock_context_manager.__aenter__.return_value = mock_client
    mock_context_manager.__aexit__.return_value = None

    with patch.object(pokeapi_service.redis_client, "get", AsyncMock(return_value=None)), \
         patch("app.services.pokeapi_service.httpx.AsyncClient", return_value=mock_context_manager):
        with pytest.raises(PokemonNotFoundException):
            await pokeapi_service.get_pokemon_by_id(9999)


@pytest.mark.anyio
async def test_get_pokemon_by_id_raises_external_api_exception_on_http_error():
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPError("boom")

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response
    mock_context_manager = AsyncMock()
    mock_context_manager.__aenter__.return_value = mock_client
    mock_context_manager.__aexit__.return_value = None

    with patch.object(pokeapi_service.redis_client, "get", AsyncMock(return_value=None)), \
         patch("app.services.pokeapi_service.httpx.AsyncClient", return_value=mock_context_manager):
        with pytest.raises(ExternalAPIException):
            await pokeapi_service.get_pokemons()
