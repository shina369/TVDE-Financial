# Usa uma imagem base do Python (pode ajustar a versão conforme necessário)
FROM python:3.10  

# Define o diretório de trabalho
WORKDIR /app  

# Instala dependências necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    pkg-config \
    gcc \
    libmysqlclient-dev \
    mysql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*  

# Copia os arquivos do projeto para o contêiner
COPY . /app  

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt  

# Define o comando de execução do app
CMD ["python", "main.py"]
