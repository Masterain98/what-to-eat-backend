import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


MYSQL_HOST = os.getenv("MYSQL_HOST", None)
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", None)
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", None)
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", None)

if None in [MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE]:
    raise RuntimeError("Missing MySQL environment variables")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
