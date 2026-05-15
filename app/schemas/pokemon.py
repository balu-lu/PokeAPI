from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class PokemonBase(BaseModel):
    name: str
    height: int
    weight: int
    types: List[str]
    sprites: Dict[str, Any]


class PokemonCreate(PokemonBase):
    pass


class PokemonUpdate(BaseModel):
    name: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    types: Optional[List[str]] = None
    sprites: Optional[Dict[str, Any]] = None


class PokemonResponse(PokemonBase):
    id: int

    class Config:
        from_attributes = True  # Essencial: diz ao Pydantic para ler objetos do SQLAlchemy
