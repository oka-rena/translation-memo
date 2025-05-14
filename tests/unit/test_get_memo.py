import json
from app.handlers.get_memo import lambda_handler

# 正常処理
class TestSuccess():
    # メモの内容を取得する（辞書型）
    def test_get_body(self, mocker):
        dummy_data = {"id": 'テスト1234', "original": "こんにちは", "translated": "Hello"}
        mocker.patch('app.handlers.get_memo.get_memo', return_value=dummy_data)

        event = json.loads('{"id": "テスト1234"}' )

        response = lambda_handler(event, None)
        status_code = response['statusCode']
        response_body = json.loads(response["body"])

        assert status_code == 200
        assert response_body.get('data') == dummy_data

    # メモの一覧を取得する（リスト型）
    def test_get_list(self, mocker):
        dummy_memo_ids = ['テストテスト1111', 'テストダミー222', 'testtdata3333']
        mocker.patch('app.handlers.get_memo.get_memo', return_value=dummy_memo_ids)

        event = json.loads('{}')

        response = lambda_handler(event, None)
        status_code = response['statusCode']
        response_body = json.loads(response["body"])
        response_list = response_body.get('data')

        assert status_code == 200
        assert set(response_list) == set(dummy_memo_ids)


# 例外処理
class TestException():
    # 取得したデータの中身がFalsyだった場合
    def test_get_falsy(self, mocker):
        dummy_data = None
        mocker.patch('app.handlers.get_memo.get_memo', return_value=dummy_data)

        event = json.loads('{"id": "テスト1234"}' )

        response = lambda_handler(event, None)
        status_code = response['statusCode']
        response_body = json.loads(response["body"])
        message = response_body.get('message')

        assert status_code == 400
        assert message == 'データが取得できませんでした'
        assert response_body.get('data') is None


    # 一覧取得が空の場合（ステータス200を返す）
    def test_get_empty_list(self, mocker):
        dummy_memo_ids = []
        mocker.patch('app.handlers.get_memo.get_memo', return_value=dummy_memo_ids)

        event = json.loads('{}')

        response = lambda_handler(event, None)
        status_code = response['statusCode']
        response_body = json.loads(response["body"])
        response_list = response_body.get('data')
        message = response_body.get('message')

        assert status_code == 200
        assert message == 'データが空です'
        assert response_list == []


    # 一覧取得が空以外のfalsy場合
    def test_get_falsy_list(self, mocker):
        dummy_memo_ids = None
        mocker.patch('app.handlers.get_memo.get_memo', return_value=dummy_memo_ids)

        event = json.loads('{}')

        response = lambda_handler(event, None)
        status_code = response['statusCode']
        response_body = json.loads(response["body"])
        response_list = response_body.get('data')
        message = response_body.get('message')

        assert status_code == 400
        assert message == 'データが取得できませんでした'
        assert response_list is None