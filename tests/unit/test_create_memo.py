# app/handler/create_memo.py のテスト
import json
from app.handlers.create_memo import lambda_handler

# 成功パターン
def test_handler_success(mocker):
    # モックを使用
    mocker.patch("app.services.translation_service.GoogleTranslator.convert", return_value="Hello")
    mocker.patch("app.handlers.create_memo.save_memo", return_value="test-memo-id")

    event = {
        "body": {
            "text": "こんにちは",
            "trans_lang": "英語",
        }
    }

    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["message"] == "保存に成功しました"
    assert body["id"] == "test-memo-id"
    assert body["translted"] == "Hello"
    print(response)


# ==== 例外処理 ====
# テキストが空の場合
def test_handler_missing_text():
    event = {
        "body": {
            "text": "",
            "trans_lang": "英語",
        }
    }

    event_body = json.loads(event["body"])
    text_origin = event_body["text"] 

    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert body["message"] == f"入力テキスト:「{text_origin}」の取得に失敗しました。空文字などは登録できません。"
    print(f"statusCode:{response["statusCode"]}", json.dumps(body, indent=4, ensure_ascii=False))

# 言語が指定されていない場合
def test_handler_missing_translang():
    event = {
        "body": {
            "text": "こんにちは",
            "trans_lang": "",
        }
    }

    event_body = json.loads(event["body"])
    trans_lang_name = event_body["trans_lang"]

    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert body["message"] == f"変換先の言語:「{trans_lang_name}」の取得に失敗しました。文字列で指定してください。"
    print(f"statusCode:{response["statusCode"]}", json.dumps(body, indent=4, ensure_ascii=False))

# 例外を発生させる
def test_handler_internal_error(mocker):
    mocker.patch("app.services.translation_service.GoogleTranslator.convert", side_effect=Exception("boom"))

    event = {
        "body": {
            "text": "こんにちは",
            "trans_lang": "英語",
        }
    }
    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 500
    assert "サーバーエラーが発生しました" in body["message"]
    print(f"statusCode:{response["statusCode"]}", json.dumps(body, indent=4, ensure_ascii=False))