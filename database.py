from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLite 
# To switch to MySQL later, just change this URL to:
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost/notes_db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./notes.db"

#connect_args={"check_same_thread": False} not needed for MySQL
engine = create_engine( SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()