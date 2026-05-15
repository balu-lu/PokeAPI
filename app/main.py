from fastapi import FastAPI
from app.api.routes import pokemons  # Mantendo o seu caminho original
from app.core.database import engine, Base

# Cria o banco de dados SQLite e as tabelas assim que a API liga
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pokedex API",
    description="API Restful em Python com operações CRUD e cache em Redis.",
    version="1.0.0"
)

# Registrando as rotas
app.include_router(pokemons.router)


@app.get("/", tags=["Health Check"])
async def root():
    return {
        "status": "online",
        "message": "Bem-vindo à Pokedex API CRUD! Acesse /docs para ver o Swagger UI."
    }
