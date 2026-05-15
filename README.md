# Pokedex API

Uma API REST desenvolvida em Python com FastAPI que consome dados da [PokeAPI](https://pokeapi.co/). O projeto aplica boas praticas de engenharia de software com cache em Redis, conteinerizacao com Docker, testes automatizados e pipeline de CI/CD.

## Funcionalidades

- Listagem paginada de Pokemons com `limit` e `offset`
- Consulta de detalhes de um Pokemon por ID
- Cache com Redis para reduzir chamadas repetidas na API externa
- Documentacao interativa com Swagger UI
- Suite de testes com boa cobertura

## Stack Tecnologica

- Python 3.10+
- FastAPI
- Poetry
- Redis
- Upstash Redis no ambiente de producao
- Docker e Docker Compose
- Pytest e pytest-cov
- GitHub Actions
- Render

## Como Rodar Localmente

### Pre-requisitos

- Docker e Docker Compose instalados
- Poetry instalado, caso queira rodar fora do container

### Clonando o repositorio

```bash
git clone https://github.com/balu-lu/PokeAPI.git
cd pokedex-api
```

### Inicie os servicos

Suba a API e o Redis com:

```bash
docker-compose -f docker/docker-compose.yml up --build
```

Depois, acesse a documentacao interativa em:

`http://localhost:8000/docs`

## Testes e Qualidade

O projeto utiliza `pytest` e `pytest-cov` para validar rotas e servicos:

```bash
poetry run pytest --cov=app tests/
```

## Deploy e CI/CD

A API esta configurada com uma esteira de CI/CD. Toda alteracao mergeada na branch `main` passa por validacoes automatizadas no GitHub Actions e, se aprovada, segue para publicacao.

No ambiente de producao hospedado no Render, foi necessario utilizar o Upstash Redis como servico externo de cache, porque o Redis local do `docker-compose` nao atende esse tipo de deploy diretamente. Assim, o projeto usa Redis Alpine localmente e Upstash em producao.

Documentacao em producao:

`https://pokeapi-nbvo.onrender.com/docs`

Endpoints documentados em producao:

- Listagem paginada: `https://pokeapi-nbvo.onrender.com/docs#/Pokemons/list_pokemons_pokemons_get`
- Busca por ID: `https://pokeapi-nbvo.onrender.com/docs#/Pokemons/get_pokemon_details_pokemons__id__get`

## Endpoints Principais

- `GET /pokemons?limit=10&offset=0`: retorna uma lista paginada de Pokemons
- `GET /pokemons/{id}`: retorna os detalhes de um Pokemon especifico
- `GET /`: health check da API

## Exemplos de Uso

### Listagem paginada

Requisicao:

```bash
curl "https://pokeapi-nbvo.onrender.com/pokemons?limit=2&offset=0"
```

Resposta:

```json
{
  "data": [
    {
      "name": "bulbasaur",
      "url": "https://pokeapi.co/api/v2/pokemon/1/"
    },
    {
      "name": "ivysaur",
      "url": "https://pokeapi.co/api/v2/pokemon/2/"
    }
  ],
  "pagination": {
    "total": 1281,
    "limit": 2,
    "offset": 0,
    "next": "/pokemons?limit=2&offset=2",
    "previous": null
  }
}
```

### Busca de Pokemon por ID

Requisicao:

```bash
curl "https://pokeapi-nbvo.onrender.com/pokemons/25"
```

Resposta:

```json
{
  "id": 25,
  "name": "pikachu",
  "height": 4,
  "weight": 60,
  "types": [
    "electric"
  ],
  "sprites": {
    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
    "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/25.png"
  }
}
```

## Estrutura do Projeto

```text
app/
  api/
    routes/
  core/
  models/
  services/
  utils/
tests/
docker/
.github/workflows/
```

## Observacoes

- O Redis e usado como camada de cache para melhorar a performance das consultas
- Em producao no Render, o cache Redis foi conectado via Upstash para viabilizar o funcionamento da aplicacao
- A documentacao do FastAPI e gerada automaticamente a partir das rotas e modelos
- Se estiver usando PowerShell no Windows, prefira comandos compativeis com esse terminal ao inves de comandos tipicos de Bash como `touch`
