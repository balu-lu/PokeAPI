# Pokedex API

Uma API REST desenvolvida em Python com FastAPI que combina consulta externa da [PokeAPI](https://pokeapi.co/) com um CRUD local em SQLite. O projeto aplica boas praticas de engenharia de software com cache em Redis, conteinerizacao com Docker, testes automatizados e pipeline de CI/CD.

## Funcionalidades

- Consulta externa paginada de Pokemons com `limit` e `offset`
- Consulta externa de detalhes de um Pokemon por ID
- CRUD local de Pokemons customizados com SQLite
- Cache com Redis para reduzir chamadas repetidas na API externa
- Persistencia local em arquivo `data/pokedex.db`
- Documentacao interativa com Swagger UI
- Suite de testes com boa cobertura

## Stack Tecnologica

- Python 3.10+
- FastAPI
- Poetry
- SQLite
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

Para rodar a API localmente:

```bash
docker compose -f docker/docker-compose.yml up --build
```

Depois, acesse a documentacao interativa em:

`http://localhost:8000/docs`

### Ambiente de desenvolvimento para testes

Se quiser rodar os testes dentro do container com dependencias de desenvolvimento:

```bash
docker compose -f docker/docker-compose.dev.yml up --build -d
```

## Testes e Qualidade

O projeto utiliza `pytest` e `pytest-cov` para validar rotas, servicos e operacoes CRUD locais.

Rodando localmente com Poetry:

```bash
poetry run pytest --cov=app tests/
```

Rodando dentro do container de desenvolvimento:

```bash
docker compose -f docker/docker-compose.dev.yml exec api pytest --cov=app tests/
```

## Deploy e CI/CD

A API esta configurada com uma esteira de CI/CD. Toda alteracao mergeada na branch `main` passa por validacoes automatizadas no GitHub Actions e, se aprovada, segue para publicacao.

No ambiente de producao hospedado no Render, foi necessario utilizar o Upstash Redis como servico externo de cache, porque o Redis local do `docker-compose` nao atende esse tipo de deploy diretamente. Assim, o projeto usa Redis Alpine localmente e Upstash em producao.

Documentacao em producao:

`https://pokeapi-nbvo.onrender.com/docs`

Endpoints documentados em producao:

- Listagem externa paginada: `https://pokeapi-nbvo.onrender.com/docs#/ðŸŒ%20Consulta%20Externa%20(PokeAPI)/list_external_pokemons_pokemons_external_get`
- Busca externa por ID: `https://pokeapi-nbvo.onrender.com/docs#/ðŸŒ%20Consulta%20Externa%20(PokeAPI)/get_external_pokemon_pokemons_external__id__get`
- CRUD local: `https://pokeapi-nbvo.onrender.com/docs#/ðŸ’¾%20Meu%20Banco%20Local%20(CRUD)`

## Endpoints Principais

- `GET /pokemons/external?limit=10&offset=0`: retorna uma lista paginada vinda da PokeAPI
- `GET /pokemons/external/{id}`: retorna os detalhes de um Pokemon da PokeAPI
- `POST /pokemons/local`: cria um Pokemon no banco local
- `GET /pokemons/local`: lista os Pokemons salvos no banco local
- `GET /pokemons/local/{pokemon_id}`: busca um Pokemon salvo localmente
- `PUT /pokemons/local/{pokemon_id}`: atualiza um Pokemon salvo localmente
- `DELETE /pokemons/local/{pokemon_id}`: remove um Pokemon salvo localmente
- `GET /`: health check da API

## Exemplos de Uso

### Listagem externa paginada

Requisicao:

```bash
curl "https://pokeapi-nbvo.onrender.com/pokemons/external?limit=2&offset=0"
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

### Busca externa de Pokemon por ID

Requisicao:

```bash
curl "https://pokeapi-nbvo.onrender.com/pokemons/external/25"
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

### Criacao de Pokemon no banco local

Requisicao:

```bash
curl -X POST "http://localhost:8000/pokemons/local" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"meu-pokemon\",\"height\":10,\"weight\":120,\"types\":[\"electric\"],\"sprites\":{\"front_default\":\"https://example.com/front.png\"}}"
```

Resposta:

```json
{
  "id": 1,
  "name": "meu-pokemon",
  "height": 10,
  "weight": 120,
  "types": [
    "electric"
  ],
  "sprites": {
    "front_default": "https://example.com/front.png"
  }
}
```

### Atualizacao de Pokemon no banco local

Requisicao:

```bash
curl -X PUT "http://localhost:8000/pokemons/local/1" \
  -H "Content-Type: application/json" \
  -d "{\"weight\":130}"
```

Resposta:

```json
{
  "id": 1,
  "name": "meu-pokemon",
  "height": 10,
  "weight": 130,
  "types": [
    "electric"
  ],
  "sprites": {
    "front_default": "https://example.com/front.png"
  }
}
```

## Estrutura do Projeto

```text
app/
  api/
    routes/
  core/
  crud/
  models/
  schemas/
  services/
  utils/
tests/
docker/
.github/workflows/
```

## Observacoes

- O Redis e usado como camada de cache para melhorar a performance das consultas externas
- O SQLite e usado para persistir os Pokemons criados localmente
- Em producao no Render, o cache Redis foi conectado via Upstash para viabilizar o funcionamento da aplicacao
- A documentacao do FastAPI e gerada automaticamente a partir das rotas e modelos
- Se estiver usando PowerShell no Windows, prefira comandos compativeis com esse terminal ao inves de comandos tipicos de Bash como `touch`
