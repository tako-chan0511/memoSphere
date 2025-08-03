from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # CORSミドルウェアをインポート
from api.routers import memos
from api import models
from api.db import engine

# データベースのテーブルを初回作成
# 注意: サーバーレス環境では、このコードはコールドスタート時に毎回実行されます。
# 本番運用では、マイグレーションツール(Alembicなど)を使うのが一般的です。
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ★ここからCORS設定を追加
origins = [
    # ここにフロントエンドのデプロイ先URLを追加します
    "https://hara0511memosphere.vercel.app",
    # ローカル開発環境も許可します
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # 全てのHTTPメソッドを許可
    allow_headers=["*"], # 全てのHTTPヘッダーを許可
)
# ★ここまでCORS設定

app.include_router(memos.router)
