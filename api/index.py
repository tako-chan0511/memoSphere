from fastapi import FastAPI
from api.routers import memos
from api import models
from api.db import engine

# データベースのテーブルを初回作成
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(memos.router)