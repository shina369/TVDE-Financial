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
    mysql-server \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copiar o script para o local correto
COPY docker-entrypoint.sh /usr/local/bin/

# Garantir permissões de execução
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Definir o script como entrypoint
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD ["python", "main.py"]
