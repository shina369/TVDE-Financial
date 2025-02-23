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

# Copiar o script de entrada
COPY docker-entrypoint.sh /usr/local/bin/

# Garantir que o script seja executável
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Definir o script de entrada
ENTRYPOINT ["docker-entrypoint.sh"]

# Comando padrão para rodar o app
CMD ["python", "main.py"]
