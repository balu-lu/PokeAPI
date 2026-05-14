from fastapi import HTTPException, status


class PokemonNotFoundException(HTTPException):
    def __init__(self, pokemon_id_or_name: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pokemon '{pokemon_id_or_name}' not found in PokeAPI."
        )


class ExternalAPIException(HTTPException):
    def __init__(self, detail: str = "Error communicating with external API"):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=detail
        )
