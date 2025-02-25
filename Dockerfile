# Usar uma imagem base menor para reduzir consumo de recursos
FROM python:3.12-slim

WORKDIR /app

# Instalar apenas as dependências essenciais
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    pkg-config \
    gcc \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/* \
    && sync && echo 3 > /proc/sys/vm/drop_caches

# Copiar apenas requirements.txt primeiro para otimizar o cache
COPY requirements.txt .

# Instalar dependências do Python
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos
COPY . .

# Copiar e garantir que o script de entrada seja executável
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Definir o script de entrada corretamente
ENTRYPOINT ["/bin/bash", "/usr/local/bin/docker-entrypoint.sh"]

# Comando padrão para rodar o app
CMD ["python", "main.py"]
