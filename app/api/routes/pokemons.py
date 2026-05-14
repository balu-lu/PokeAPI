from fastapi import APIRouter, Query, Path
from app.services import pokeapi_service
from app.models.pokemon import PokemonPaginatedResponse, PokemonDetail

router = APIRouter(prefix="/pokemons", tags=["Pokemons"])


@router.get("", response_model=PokemonPaginatedResponse)
async def list_pokemons(
    limit: int = Query(
        10, ge=1, le=100, description="Número de itens por página"),
    offset: int = Query(0, ge=0, description="Número de itens para pular")
):
    """
    Retorna uma lista paginada de Pokémons.
    """
    return await pokeapi_service.get_pokemons(limit=limit, offset=offset)


@router.get("/{id}", response_model=PokemonDetail)
async def get_pokemon_details(
    id: int = Path(..., description="ID do Pokémon (ex: 25 para Pikachu)", gt=0)
):
    """
    Retorna os detalhes de um Pokémon específico pelo seu ID.
    """
    return await pokeapi_service.get_pokemon_by_id(id)
