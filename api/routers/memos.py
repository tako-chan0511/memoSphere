from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api import models, schemas
from api.db import get_db
from typing import List # Listをインポート

router = APIRouter()

@router.get("/api/memos", response_model=List[schemas.Memo])
def get_all_memos(db: Session = Depends(get_db)):
    """全てのメモをデータベースから取得するAPI"""
    memos = db.query(models.Memo).all()
    return memos

@router.get("/api/memos/{memo_id}", response_model=schemas.Memo)
def get_memo(memo_id: int, db: Session = Depends(get_db)):
    """指定されたIDのメモを1件取得するAPI"""
    memo = db.query(models.Memo).filter(models.Memo.id == memo_id).first()
    if not memo:
        raise HTTPException(status_code=404, detail="Memo not found")
    return memo

@router.post("/api/memos", status_code=status.HTTP_201_CREATED, response_model=schemas.Memo)
def create_memo(memo_data: schemas.MemoCreate, db: Session = Depends(get_db)):
    """新しいメモをデータベースに保存するAPI"""
    new_memo = models.Memo(task=memo_data.task, status=memo_data.status)
    db.add(new_memo)
    db.commit()
    db.refresh(new_memo)
    return new_memo

@router.patch("/api/memos/{memo_id}", response_model=schemas.Memo)
def update_memo(memo_id: int, memo_data: schemas.MemoUpdate, db: Session = Depends(get_db)):
    """指定されたIDのメモの内容やステータスを更新する"""
    memo_to_update = db.query(models.Memo).filter(models.Memo.id == memo_id).first()
    if not memo_to_update:
        raise HTTPException(status_code=404, detail="Memo not found")
    
    # リクエストで送られてきた項目のみを更新する
    if memo_data.task is not None:
        memo_to_update.task = memo_data.task
    if memo_data.status is not None:
        memo_to_update.status = memo_data.status
    
    db.commit()
    db.refresh(memo_to_update)
    return memo_to_update

@router.delete("/api/memos/{memo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_memo(memo_id: int, db: Session = Depends(get_db)):
    """指定されたIDのメモを削除するAPI"""
    memo_to_delete = db.query(models.Memo).filter(models.Memo.id == memo_id).first()
    if not memo_to_delete:
        raise HTTPException(status_code=404, detail="Memo not found")
    
    db.delete(memo_to_delete)
    db.commit()
    return
