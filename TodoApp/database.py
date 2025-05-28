from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base #used to be sqlalchemy.ext.declarative
#SQLALCHEMY_DATABASE_URL='postgresql://postgres:test1234@localhost/TodoApplicationDatabase'

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

#engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()