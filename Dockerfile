FROM python:3.11-slim

# Instala as dependências de sistema necessárias para o WeasyPrint
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# O Render define a porta via variável de ambiente PORT, por isso usamos 0.0.0.0
CMD ["python", "app.py"]
