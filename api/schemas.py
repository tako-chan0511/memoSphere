from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# 更新用のスキーマ (入力) - statusを任意項目として追加
class MemoUpdate(BaseModel):
    task: Optional[str] = None
    status: Optional[str] = None

# 作成用のスキーマ (入力)
class MemoCreate(BaseModel):
    task: str
    status: str = 'Not started'

# レスポンス用のスキーマ (出力)
class Memo(BaseModel):
    id: int
    task: str
    status: str
    created_at: datetime
    updated_at: datetime

    # SQLAlchemy 2.0+ Pydantic v2+ での推奨設定
    model_config = ConfigDict(from_attributes=True)
