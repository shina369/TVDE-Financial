# Usa uma imagem base completa e estável do Python
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Atualiza os repositórios e instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev pkg-config gcc libmariadb-dev curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia os arquivos do projeto para o contêiner
COPY . .

# Instala as dependências do projeto
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Define o comando padrão para iniciar o app
CMD ["python3", "main.py"]