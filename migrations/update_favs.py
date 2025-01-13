from sqlalchemy import create_engine, text
from app.config import DATABASE_URL

def update_database():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        # Actualizar la columna favs a JSON
        connection.execute(text("""
            ALTER TABLE users 
            ALTER COLUMN favs TYPE jsonb USING CASE 
                WHEN favs IS NULL THEN '[]'::jsonb
                ELSE favs::jsonb
            END;
        """))
        connection.commit()

if __name__ == "__main__":
    update_database() 