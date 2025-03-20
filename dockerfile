# Usar uma imagem base adequada
FROM python:3.10-slim

# Definir ambiente não interativo para evitar prompts
ENV DEBIAN_FRONTEND=noninteractive 

# Instalar dependências
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential python3-dev pkg-config gcc \
    default-libmysqlclient-dev mysql-client && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY . /app

# Instalar dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta usada pelo app (se necessário)
EXPOSE 8501  

# Comando para rodar o app
CMD ["python", "main.py"]
