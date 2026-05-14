from fastapi import FastAPI
from app.api.routes import pokemons

app = FastAPI(
    title="Pokedex API",
    description="API Restful em Python que consome dados da PokeAPI com cache em Redis.",
    version="1.0.0"
)

# Registrando as rotas
app.include_router(pokemons.router)


@app.get("/", tags=["Health Check"])
async def root():
    return {
        "status": "online",
        "message": "Bem-vindo à Pokedex API! Acesse /docs para ver o Swagger UI."
    }
