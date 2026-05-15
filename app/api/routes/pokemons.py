from fastapi import APIRouter, Query, Path, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Importações da PokeAPI Externa
from app.services import pokeapi_service
from app.models.pokemon import PokemonPaginatedResponse, PokemonDetail

# Importações do Banco Local
from app.core.database import get_db
from app.schemas.pokemon import PokemonCreate, PokemonResponse, PokemonUpdate
from app.crud import pokemon as crud
from app.models.pokemon_db import PokemonDB

router = APIRouter(prefix="/pokemons")

# ==========================================
# 🌐 ROTAS EXTERNAS (PokeAPI + Redis)
# ==========================================


@router.get("/external", response_model=PokemonPaginatedResponse, tags=["🌐 Consulta Externa (PokeAPI)"])
async def list_external_pokemons(
    limit: int = Query(
        10, ge=1, le=100, description="Número de itens por página"),
    offset: int = Query(0, ge=0, description="Número de itens para pular")
):
    """
    Retorna uma lista paginada buscando diretamente da PokeAPI oficial.
    """
    return await pokeapi_service.get_pokemons(limit=limit, offset=offset)


@router.get("/external/{id}", response_model=PokemonDetail, tags=["🌐 Consulta Externa (PokeAPI)"])
async def get_external_pokemon(
    id: int = Path(..., description="ID oficial do Pokémon", gt=0)
):
    """
    Retorna os detalhes de um Pokémon específico usando a PokeAPI oficial.
    """
    return await pokeapi_service.get_pokemon_by_id(id)

# ==========================================
# 💾 ROTAS CRUD (Banco de Dados Local SQLite)
# ==========================================


@router.post("/local", response_model=PokemonResponse, status_code=status.HTTP_201_CREATED, tags=["💾 Meu Banco Local (CRUD)"])
def create_local_pokemon(pokemon: PokemonCreate, db: Session = Depends(get_db)):
    """
    Salva um novo Pokémon customizado no banco de dados SQLite.
    """
    db_pokemon = crud.get_pokemon_by_name(db, name=pokemon.name)
    if db_pokemon:
        raise HTTPException(
            status_code=400, detail="Pokémon já cadastrado no banco local.")
    return crud.create_pokemon(db=db, pokemon=pokemon)


@router.get("/local", response_model=List[PokemonResponse], tags=["💾 Meu Banco Local (CRUD)"])
def list_local_pokemons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista todos os Pokémons criados e salvos no seu banco de dados local.
    """
    return crud.get_all_pokemons(db, skip=skip, limit=limit)


@router.get("/local/{pokemon_id}", response_model=PokemonResponse, tags=["💾 Meu Banco Local (CRUD)"])
def get_local_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    """
    Busca um Pokémon específico pelo ID gerado no seu banco de dados local.
    """
    db_pokemon = crud.get_pokemon_by_id(db, pokemon_id=pokemon_id)
    if not db_pokemon:
        raise HTTPException(
            status_code=404, detail="Pokémon não encontrado no banco local.")
    return db_pokemon


@router.put("/local/{pokemon_id}", response_model=PokemonResponse, tags=["💾 Meu Banco Local (CRUD)"])
def update_local_pokemon(pokemon_id: int, pokemon_in: PokemonUpdate, db: Session = Depends(get_db)):
    """
    Atualiza as informações de um Pokémon no banco de dados local.
    """
    db_pokemon = db.query(PokemonDB).filter(PokemonDB.id == pokemon_id).first()
    if not db_pokemon:
        raise HTTPException(
            status_code=404, detail="Pokémon não encontrado no banco local.")
    return crud.update_pokemon(db=db, db_pokemon=db_pokemon, pokemon_update=pokemon_in)


@router.delete("/local/{pokemon_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["💾 Meu Banco Local (CRUD)"])
def delete_local_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    """
    Deleta permanentemente um Pokémon do banco de dados local.
    """
    db_pokemon = db.query(PokemonDB).filter(PokemonDB.id == pokemon_id).first()
    if not db_pokemon:
        raise HTTPException(
            status_code=404, detail="Pokémon não encontrado no banco local.")
    crud.delete_pokemon(db=db, db_pokemon=db_pokemon)
    return None
