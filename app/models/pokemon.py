from pydantic import BaseModel, HttpUrl
from typing import List, Optional

# Schema para os Sprites


class PokemonSprites(BaseModel):
    front_default: Optional[HttpUrl]
    back_default: Optional[HttpUrl]

# Schema de Detalhes do Pokemon (GET /pokemons/{id})


class PokemonDetail(BaseModel):
    id: int
    name: str
    height: int
    weight: int
    types: List[str]
    sprites: PokemonSprites

# Schemas para Paginação (GET /pokemons)


class PaginationInfo(BaseModel):
    total: int
    limit: int
    offset: int
    next: Optional[str]
    previous: Optional[str]


class PokemonListItem(BaseModel):
    name: str
    url: str


class PokemonPaginatedResponse(BaseModel):
    data: List[PokemonListItem]
    pagination: PaginationInfo
