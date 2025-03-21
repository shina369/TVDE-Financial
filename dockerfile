# Usar uma imagem base mais completa
FROM python:3.10

# Definir ambiente não interativo
ENV DEBIAN_FRONTEND=noninteractive 

# Atualizar pacotes e instalar dependências
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev pkg-config gcc default-libmysqlclient-dev libmysqlclient-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto
COPY . /app

# Instalar dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta usada pelo app (se necessário)
EXPOSE 8501

# Comando para rodar o app
CMD ["python", "main.py"]
