# Stage 1: Builder
FROM python:3.10-slim as builder

ARG INSTALL_DEV=false

# Evita a criação de ficheiros .pyc e mantém o output no terminal
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependências do sistema necessárias para o Poetry
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copiar apenas os ficheiros de dependência primeiro para aproveitar o cache do Docker
COPY pyproject.toml poetry.lock* ./

# Instalar dependências do projeto sem criar virtualenv.
# Em desenvolvimento, também instalamos o grupo `dev` para disponibilizar o pytest.
RUN poetry config virtualenvs.create false \
    && if [ "$INSTALL_DEV" = "true" ]; then poetry install --with dev --no-interaction --no-ansi; else poetry install --only main --no-interaction --no-ansi; fi

# Stage 2: Imagem Final
FROM python:3.10-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Criar um utilizador non-root para segurança
RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

# Instalar curl para o healthcheck na imagem final
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar os pacotes instalados do stage builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar o código da aplicação
COPY ./app ./app

# Mudar a propriedade dos ficheiros para o utilizador non-root
RUN chown -R appuser:appuser /app
USER appuser

# Healthcheck para verificar se a API está a responder
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
