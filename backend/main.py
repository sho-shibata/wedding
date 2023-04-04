from fastapi import FastAPI
import os

from routers import user as userRouter
from models import user as userModels

from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from dotenv import load_dotenv

# 環境ファイルの読み込み
load_dotenv('setting/.env')

userModels.BaseModel.metadata.create_all(bind=engine)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# オリジン
ROOT_BACK = os.environ['ROOT']
ROOT_FRONT = os.environ['ROOT_FRONT']

origins = [
    ROOT_BACK,
    ROOT_FRONT
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userRouter.router)
