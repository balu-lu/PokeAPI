from sqlalchemy.orm import Session
from app.models.pokemon_db import PokemonDB
from app.schemas.pokemon import PokemonCreate, PokemonUpdate


def create_pokemon(db: Session, pokemon: PokemonCreate):
    db_pokemon = PokemonDB(**pokemon.model_dump())
    db.add(db_pokemon)
    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon


def get_pokemon_by_name(db: Session, name: str):
    return db.query(PokemonDB).filter(PokemonDB.name == name).first()


def update_pokemon(db: Session, db_pokemon: PokemonDB, pokemon_update: PokemonUpdate):
    update_data = pokemon_update.model_dump(
        exclude_unset=True)  # Atualiza só o que foi enviado
    for key, value in update_data.items():
        setattr(db_pokemon, key, value)

    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon


def delete_pokemon(db: Session, db_pokemon: PokemonDB):
    db.delete(db_pokemon)
    db.commit()


def get_pokemon_by_id(db: Session, pokemon_id: int):
    return db.query(PokemonDB).filter(PokemonDB.id == pokemon_id).first()


def get_all_pokemons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PokemonDB).offset(skip).limit(limit).all()
