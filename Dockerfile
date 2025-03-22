# Usa uma imagem base oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Atualiza os repositórios e instala pacotes necessários
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev pkg-config gcc default-libmysqlclient-dev libmysqlclient-dev curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia os arquivos do projeto para o contêiner
COPY . .

# Atualiza o pip e instala as dependências do projeto
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Define o comando padrão para iniciar o app
CMD ["python", "app.py"]
