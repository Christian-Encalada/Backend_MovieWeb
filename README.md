# Proyecto Final - Clasificación de Usuarios por Gustos

Este proyecto utiliza FastAPI, SQLAlchemy y Alembic para crear una API que permite clasificar a los usuarios por sus gustos en películas.

## Requisitos

- Python 3.8+
- PostgreSQL
- pipenv (opcional, para gestionar el entorno virtual)

## Instalación

1. Clona el repositorio:

```sh
git clone <URL_DEL_REPOSITORIO>

```
2. Crea y activa un entorno virtual:
```sh
python -m venv .venv
source .venv/bin/activate  # En Windows usa `.venv\Scripts\activate`

```
3. Instala las dependencias:
```sh
pip install -r requirements.txt

```
4. Configura las variables de entorno en un archivo .env:
```sh

DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
SSL_CERT=

```
4. Hacer migraciones
```sh

alembic revision --autogenerate -m "add name-migration"
alembic upgrade head

```
5. Inicia el servidor de desarrollo:
```sh

uvicorn app.main:app --reload

```
6. Swagger:
```sh

Accede a la documentación interactiva de la API en http://127.0.0.1:8000/docs.

