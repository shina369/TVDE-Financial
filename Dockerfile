FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev pkg-config gcc libmariadb-dev curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

RUN python -m venv /opt/venv
RUN /opt/venv/bin/pip install --upgrade pip
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

EXPOSE 52230

CMD ["/opt/venv/bin/python", "main.py"]
