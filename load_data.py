from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.services.data_loader import load_movies_data, load_links_data
from app.models.movie import Movie
from app.models.link import Link

def main():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    load_movies_data(db)
    load_links_data(db)
    db.close()

if __name__ == "__main__":
    main()