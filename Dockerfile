# Use a imagem do MySQL 8.0 diretamente
FROM debian:bookworm

# Instalar dependências do sistem

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev pkg-config gcc default-libmysqlclient-dev mysql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar o script de entrada
COPY docker-entrypoint.sh /usr/local/bin/

# Garantir permissões de execução
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Definir o script como entrypoint
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Definir o comando padrão
CMD ["python", "main.py"]
