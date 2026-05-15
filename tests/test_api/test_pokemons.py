from unittest.mock import patch
from app.utils.exceptions import PokemonNotFoundException

# Dados falsos (mocks) para simular o retorno do nosso service
MOCK_POKEMON_LIST = {
    "data": [
        {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
        {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"}
    ],
    "pagination": {
        "total": 1281,
        "limit": 2,
        "offset": 0,
        "next": "/pokemons?limit=2&offset=2",
        "previous": None
    }
}

MOCK_POKEMON_DETAIL = {
    "id": 25,
    "name": "pikachu",
    "height": 4,
    "weight": 60,
    "types": ["electric"],
    "sprites": {
        "front_default": "http://example.com/front.png",
        "back_default": "http://example.com/back.png"
    }
}


@patch("app.api.routes.pokemons.pokeapi_service.get_pokemons")
def test_list_pokemons(mock_get_pokemons, client):
    # Configuramos o mock para retornar nossos dados falsos
    mock_get_pokemons.return_value = MOCK_POKEMON_LIST

    response = client.get("/pokemons/external?limit=2&offset=0")

    assert response.status_code == 200
    json_response = response.json()
    assert "data" in json_response
    assert "pagination" in json_response
    assert len(json_response["data"]) == 2
    assert json_response["pagination"]["total"] == 1281


@patch("app.api.routes.pokemons.pokeapi_service.get_pokemon_by_id")
def test_get_pokemon_details(mock_get_pokemon_by_id, client):
    mock_get_pokemon_by_id.return_value = MOCK_POKEMON_DETAIL

    response = client.get("/pokemons/external/25")

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["name"] == "pikachu"
    assert json_response["id"] == 25
    assert "electric" in json_response["types"]


@patch("app.api.routes.pokemons.pokeapi_service.get_pokemon_by_id")
def test_get_pokemon_not_found(mock_get_pokemon_by_id, client):
    # Simulamos o disparo de uma exceção quando o pokemon não existe
    mock_get_pokemon_by_id.side_effect = PokemonNotFoundException("9999")

    response = client.get("/pokemons/external/9999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_root_healthcheck(client):
    response = client.get("/")

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "online"
    assert "/docs" in json_response["message"]
