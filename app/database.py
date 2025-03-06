from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import Session


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/petik'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close 