FROM python:3.12-slim

WORKDIR /app

# Instalar as dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev \
    pkg-config \
    gcc \
    libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/* && \
    sync && \
    echo 3 > /proc/sys/vm/drop_caches

# Copiar os arquivos do projeto
COPY . .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o script de entrada
COPY docker-entrypoint.sh /usr/local/bin/

# Garantir que o script seja executável
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Definir o script de entrada
ENTRYPOINT ["docker-entrypoint.sh"]

# Comando padrão para rodar o app
CMD ["python", "main.py"]
