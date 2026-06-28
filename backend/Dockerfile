# Gebruik een officiële, lichte Python runtime
FROM python:3.10-slim

# Stel de werkomgeving in binnen de container
WORKDIR /backend

# Voorkom dat Python .pyc bestanden schrijft naar schijf
ENV PYTHONDONTWRITEBYTECODE 1
# Zorg dat console outputs direct geprint worden zonder buffering
ENV PYTHONUNBUFFERED 1

# Kopieer eerst alleen de requirements om optimaal gebruik te maken van Docker caching
COPY requirements.txt .

# Installeer de packages
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer de rest van de backend applicatiecode
COPY . .

# Exposeer de poort waarop FastAPI draait
EXPOSE 8000

# Start de applicatie middels Uvicorn via de juiste module-route
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]