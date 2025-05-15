import json
from app.handlers.delete_memo import lambda_handler

# 正常処理
def test_delete_success(mocker):
    dummy_response = json.dumps({
        "statusCode": 200,
        "message": "データの削除が完了しました"
    }, ensure_ascii=False)
    mocker.patch('app.handlers.delete_memo.delete_memo', return_value=dummy_response)

    event = {'id': 'test-id'}

    response = lambda_handler(event, None)
    assert response == json.loads(dummy_response)


# 例外処理
# 渡されたidがfalsyならエラーを返す
def test_delete_not_id(mocker):
    dummy_response = json.dumps({
        "statusCode": 400,
        "message": "error!: データが見つかりませんでした"
    }, ensure_ascii=False)
    mocker.patch('app.handlers.delete_memo.delete_memo', return_value=dummy_response)

    event = {'id': ''}

    response = lambda_handler(event, None)
    assert response == json.loads(dummy_response)