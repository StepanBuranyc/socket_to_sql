FROM python:3.9-slim

# Instalace pyodbc a potřebných balíčků
RUN apt-get update && apt-get install -y unixodbc-dev && pip install pyodbc

# Nastavení pracovního adresáře
WORKDIR /app

# Zkopírování aplikace
COPY socket_server.py .

# Otevření portu
EXPOSE 5000

# Spuštění aplikace
CMD ["python", "socket_server.py"]
