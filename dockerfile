# Usar uma imagem base leve do Python
FROM python:3.10-slim

# Definir ambiente não interativo para evitar prompts durante o build
ENV DEBIAN_FRONTEND=noninteractive 

# Atualizar pacotes e instalar dependências necessárias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev \
    pkg-config \
    gcc \
    default-libmysqlclient-dev \
    mysql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para o diretório de trabalho
COPY . /app

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que o app vai rodar (ajuste conforme sua necessidade)
EXPOSE 52230

# Comando para rodar o app
CMD ["python", "main.py"]
