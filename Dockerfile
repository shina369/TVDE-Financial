FROM python:3.12

WORKDIR /app

# Instalar as dependências do sistema
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    python3-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar os arquivos do projeto
COPY . .

# Instalar os pacotes do Python
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]

COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]

RUN chmod +x /caminho/do/docker-entrypoint.sh
