# Usa uma imagem base leve e estável do Python
FROM python:3.9-slim-bookworm

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    python3-dev pkg-config gcc libmariadb-dev curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Cria usuário não-root
RUN useradd -m appuser

# Cria ambiente virtual e instala dependências
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Define usuário não-root
USER appuser

# Expõe a porta configurada
EXPOSE 52230

# Comando de inicialização
CMD ["python", "main.py"]