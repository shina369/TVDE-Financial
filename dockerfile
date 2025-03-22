# Usar uma imagem base leve do Python
FROM python:3.10-slim

# Definir ambiente não interativo para evitar prompts durante o build
ENV DEBIAN_FRONTEND=noninteractive 

# Criar diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para o diretório de trabalho
COPY . /app

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que o app vai rodar (ajuste conforme sua necessidade)
EXPOSE 8501

# Comando para rodar o app
CMD ["python", "main.py"]
