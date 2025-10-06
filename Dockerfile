# ============================================================================
# SafeBot Chainlit - Dockerfile
# ============================================================================
# Multi-stage build para otimizar o tamanho da imagem final
# ============================================================================

# Stage 1: Builder - Instala dependências
FROM python:3.12-slim AS builder

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias para build
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry --version

# Copiar apenas arquivos de dependências primeiro (cache Docker)
COPY pyproject.toml poetry.lock* ./

# Instalar dependências (sem dev dependencies)
RUN poetry install --no-root --no-dev && rm -rf $POETRY_CACHE_DIR

# ============================================================================
# Stage 2: Runtime - Imagem final otimizada
# ============================================================================
FROM python:3.12-slim AS runtime

# Metadados da imagem
LABEL maintainer="SafeBot Team"
LABEL description="SafeBot - Sistema Inteligente de Segurança do Trabalho"
LABEL version="1.0.0"

# Criar usuário não-root para segurança
RUN useradd -m -u 1000 safebot && \
    mkdir -p /app && \
    chown -R safebot:safebot /app

# Definir diretório de trabalho
WORKDIR /app

# Instalar apenas dependências runtime essenciais
RUN apt-get update && apt-get install -y \
    libsqlite3-0 \
    && rm -rf /var/lib/apt/lists/*

# Copiar o ambiente virtual do builder
COPY --from=builder --chown=safebot:safebot /app/.venv /app/.venv

# Copiar o código da aplicação
COPY --chown=safebot:safebot . .

# Garantir que os diretórios necessários existem e têm permissões corretas
RUN mkdir -p /app/tmp/chromadb /app/data/pdfs /app/.chainlit && \
    chown -R safebot:safebot /app/tmp /app/data /app/.chainlit && \
    chmod -R 755 /app/tmp /app/data /app/.chainlit

# Mudar para usuário não-root
USER safebot

# Configurar PATH para usar o virtualenv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Expor porta do Chainlit
EXPOSE 8000

# Healthcheck para verificar se a aplicação está respondendo
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000').read()" || exit 1

# Comando padrão para iniciar a aplicação
CMD ["chainlit", "run", "chainlit_app.py", "--host", "0.0.0.0", "--port", "8000"]
