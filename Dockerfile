FROM python:3.12-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas o requirements.txt primeiro
COPY requirements.txt .

# Instalar pacotes do Python
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copiar os arquivos do projeto
COPY . .

# Copiar o script de entrada
COPY docker-entrypoint.sh /usr/local/bin/

# Garantir que o script seja executável
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Definir o script de entrada corretamente
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Comando padrão para rodar o app
CMD ["python", "main.py"]
