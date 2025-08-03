from fastapi.testclient import TestClient
from api.index import app # メインのFastAPIアプリケーションをインポート

# テスト用のクライアントを作成
client = TestClient(app)

def test_get_all_memos():
    """
    GET /api/memos のテスト
    正常なレスポンス（ステータスコード200）が返ってくることを確認する
    """
    # APIエンドポイントにリクエストを送信
    response = client.get("/api/memos")
    
    # ステータスコードが200であることを検証
    assert response.status_code == 200
    
    # レスポンスのボディがリスト形式（JSON配列）であることを検証
    assert isinstance(response.json(), list)