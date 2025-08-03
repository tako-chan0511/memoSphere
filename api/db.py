import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# .envファイルから環境変数を読み込む
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# サーバーレス環境での接続プールに関する推奨設定を追加
engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DBセッションを取得するための依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
