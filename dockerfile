# Utilizar una imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar las dependencias necesarias para psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev

# Copiar los archivos de requisitos
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY . .

# Copiar el archivo alembic.ini
COPY alembic.ini /app/alembic.ini

# Establecer las variables de entorno
ENV DB_USER=proyecto_ia
ENV DB_PASSWORD=Pucem.2024
ENV DB_HOST=proyecto-ia-pucem.postgres.database.azure.com
ENV DB_PORT=5432
ENV DB_NAME=postgres
ENV SSL_CERT=./ssl/DigiCertGlobalRootG2.crt.pem

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]