from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL="postgresql+psycopg://swaragreddy@localhost:5432/project1"

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind = engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
