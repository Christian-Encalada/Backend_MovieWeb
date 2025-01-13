import sys
import os
from pathlib import Path

# Agregar el directorio raíz del proyecto al PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.models.user import User
from app.core.security import get_password_hash

load_dotenv()

# Configuración de la base de datos
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def hash_existing_passwords():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        for user in users:
            # Solo hashear si la contraseña no está ya hasheada
            if not user.password.startswith('$2b$'):
                hashed_password = get_password_hash(user.password)
                user.password = hashed_password
        db.commit()
        print("Contraseñas hasheadas exitosamente")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    hash_existing_passwords() 