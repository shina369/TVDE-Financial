FROM python:3.12-slim

WORKDIR /app

# Definir o ambiente para não interagir manualmente com o apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Instalar as dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    pkg-config \
    gcc \
    default-libmysqlclient-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copiar os arquivos do projeto
COPY . .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Garantir que o script seja executável (se necessário)
# Removido porque docker-entrypoint.sh não existe
# RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Definir o comando padrão para rodar o app
CMD ["python", "main.py"]
