FROM python:3.12-slim

WORKDIR /app

# Instalar as dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    pkg-config \
    gcc \
    libmysqlclient-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


# Copiar os arquivos do projeto
COPY . .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Garantir que o script seja executável
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Definir o script de entrada
ENTRYPOINT ["docker-entrypoint.sh"]

# Comando padrão para rodar o app
CMD ["python", "main.py"]
