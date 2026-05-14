### Construir API Restful em python que consuma dados da https://pokeapi.co/ e os disponibilize de forma paginada. A API deverá estar dockerizada, testada com CI/CD configurado, e piblicada em um serviço de deploy.

--

### REQS Tecnicos

## Lingugagem
    - Python   
    - FastAPI

## Consumo de Dados
a API deve consumir dados da https://pokeapi.co/
armazenamnto local (opcional): pode fazer cache local para performance, mas o consumo deve ser da PokeAPI originalmente

## ENDPOINTS MINIMOS
    `GET    /pokemons`: lista de pokemons paginada
    `GET    /pokemons/{id}`: detalhes do pokemon

## Paginação
o endpoint `/pokemons` deve aceitar:
    - query param `limit`(default=10), ou `page_size`
    a resposta deve incluir:
```json
{
    "data": [],
    "pagination": {
        "total": 1281,
        "limit": 20,
        "offset": 0,
        "next": "/pokemons?limit=20&offset=20",
        "previous": null
    }
}
```

## FORMATO DO JSON de RESPOSTA
Para o endpoint `/pokemons`:
```json
{
    "name": "pikachu",
    "id": 25,
    "height": 4,
    "weight": 60,
    "types": ["electric"],
    "sprites": {
        "front_default": "https://raw.githubusercontent.com/...",
        "back_default": "https://raw.githubusercontent.com/..."
    }
}
```
os dados devem ser extraidos diretamente da PokeAPI

## DOCKER
Criar um `Dockerfile` funcional
criar um `docker-compose.yml` se houver necessidade de serviços adicionais (ex: cache, banco)

## TESTES UNITARIOS
Escrever testes com *pytest*
cobrir pelo menos:
    - Resposta dos endpoints
    - Paginação
    - Erros (ex: pokemon not found)
Gerar relatrio de cobertura com `pytest-cov`

## CI/CD
Configurar workflow de CI/CD com *GitHub Action*
etápas minimas do CI:
    - Instalação de dependencias
    - Execucção dos testes
    - Verificação de cobertura
    - Lint (opcional)
Etapas do CD:
    - Deploy automatico após ``push`` na branch principal

## DEPLOY
Publicar a API em um serviço gratuito como:
    - [Render]
    ...
O endereço final da API deve estar acessivel publicamente

## Integração CI/CD com deploy
O deploy deve acontecer automaticamente via pipeline configurada no GitHub Actions

## DOCUMETNAÇÂO
Utilizar a docimentação automatica do *FastAPI (swagger UI)*
Incluir um ``README.md`` com:
    - Descrição do prijeto
    - como rodar localmente
    - como executar testes
    - link de produção (API em prod)
    - Exemplo de requisição e resposta da API

---

## EXTRAS (DESEJAVEIS)
Cache Local (redis)
tratamenteo de exceções personalizado
rate limiting ou autenticação simples (via API key)
logs estruturados
uso do ``pydantic`` para validação de dados
