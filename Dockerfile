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

# Cria um ambiente virtual e ativa
RUN python -m venv /opt/venv

# Instala as dependências no ambiente virtual
RUN /opt/venv/bin/pip install --upgrade pip
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
RUN /opt/venv/bin/pip install --no-cache-dir flet[all]==0.28.3

# Expõe a porta que o Flet vai usar (geralmente a porta 8551 para Flet, mas use 52230 conforme sua configuração)
EXPOSE 52230

# Define o comando para rodar o app com Flet no ambiente virtual
CMD ["/opt/venv/bin/python", "main.py"]
