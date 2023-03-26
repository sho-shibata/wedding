from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 環境ファイルの読み込み
load_dotenv('setting/.env')

user = os.environ['DB_USER']
password = os.environ['DB_PASS']
host = os.environ['DB_HOST']
port = os.environ['DB_PORT']
db_name = os.environ['DB_NAME']

SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, echo_pool=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()
