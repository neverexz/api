from sqlite3 import SQLITE_ABORT
from venv import create
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/petik'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

