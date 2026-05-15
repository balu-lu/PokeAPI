def test_create_local_pokemon(client):
    payload = {
        "name": "Bulbasaur",
        "height": 7,
        "weight": 69,
        "types": ["grass", "poison"],
        "sprites": {"front_default": "url_do_bulbasaur"}
    }
    response = client.post("/pokemons/local", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Bulbasaur"
    assert data["id"] is not None


def test_create_duplicate_pokemon(client):
    payload = {"name": "Mew", "height": 4, "weight": 40,
               "types": ["psychic"], "sprites": {}}
    client.post("/pokemons/local", json=payload)

    response = client.post("/pokemons/local", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Pokémon já cadastrado no banco local."


def test_list_local_pokemons(client):
    response = client.get("/pokemons/local")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_local_pokemons_respects_skip_and_limit(client):
    payloads = [
        {"name": "Charmander", "height": 6, "weight": 85, "types": ["fire"], "sprites": {}},
        {"name": "Squirtle", "height": 5, "weight": 90, "types": ["water"], "sprites": {}},
    ]
    for payload in payloads:
        client.post("/pokemons/local", json=payload)

    response = client.get("/pokemons/local?skip=1&limit=1")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Squirtle"


def test_get_local_pokemon_by_id(client):
    payload = {"name": "Pikachu", "height": 4,
               "weight": 60, "types": ["electric"], "sprites": {}}
    create_resp = client.post("/pokemons/local", json=payload)
    pokemon_id = create_resp.json()["id"]

    response = client.get(f"/pokemons/local/{pokemon_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Pikachu"


def test_get_local_pokemon_not_found(client):
    response = client.get("/pokemons/local/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Pokémon não encontrado no banco local."


def test_update_local_pokemon(client):
    payload = {"name": "Charmander", "height": 6,
               "weight": 85, "types": ["fire"], "sprites": {}}
    create_resp = client.post("/pokemons/local", json=payload)
    pokemon_id = create_resp.json()["id"]

    update_payload = {"weight": 90}
    response = client.put(f"/pokemons/local/{pokemon_id}", json=update_payload)

    assert response.status_code == 200
    assert response.json()["weight"] == 90
    assert response.json()["name"] == "Charmander"


def test_update_local_pokemon_not_found(client):
    response = client.put("/pokemons/local/9999", json={"weight": 90})

    assert response.status_code == 404
    assert response.json()["detail"] == "Pokémon não encontrado no banco local."


def test_delete_local_pokemon(client):
    payload = {"name": "Squirtle", "height": 5,
               "weight": 90, "types": ["water"], "sprites": {}}
    create_resp = client.post("/pokemons/local", json=payload)
    pokemon_id = create_resp.json()["id"]

    response = client.delete(f"/pokemons/local/{pokemon_id}")
    assert response.status_code == 204

    get_response = client.get(f"/pokemons/local/{pokemon_id}")
    assert get_response.status_code == 404


def test_delete_local_pokemon_not_found(client):
    response = client.delete("/pokemons/local/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Pokémon não encontrado no banco local."
