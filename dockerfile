# Atualiza os repositórios e instala pacotes necessários
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    pkg-config \
    gcc \
    libmysqlclient-dev \
    mysql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*