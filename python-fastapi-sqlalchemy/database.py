from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Aggiungi "+psycopg2" dopo postgresql
DATABASE_URL = "postgresql+psycopg2://devuser:devpassword@localhost:5432/sampledb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
