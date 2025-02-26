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

# Dar permissão ao script de entrada
RUN chmod +x /app/docker-entrypoint.sh

# Definir o script de entrada e o comando padrão para rodar o app
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["python", "main.py"]
