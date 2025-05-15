import pytest
from app.handlers.update_memo import lambda_handler

# 成功処理
def test_update_memo_success(mocker):
    dummy_id = 'テスト1111'
    text_origin = 'テキストだよ'
    origin_lang_name = '日本語'
    trans_lang_name = '英語'

    dummy_update_result = {
        "statusCode": 200,
        "message": f"id:{dummy_id} のデータを書き換えました。"
    }
    mocker.patch('app.handlers.update_memo.update_memo', return_value=dummy_update_result)
    mocker.patch('app.services.translation_service.GoogleTranslator.convert', return_value='this is text')

    event = {
        'id': dummy_id,
        'body': {
            'text': text_origin,
            'origin_lang': origin_lang_name,
            'trans_lang': trans_lang_name
        }
    }

    response = lambda_handler(event, None)
    assert response == dummy_update_result


# 例外処理
# データの書き換えが行えなかった場合
def test_update_error(mocker):
    dummy_id = 'テスト1111'
    text_origin = 'テキストだよ'
    origin_lang_name = '日本語'
    trans_lang_name = '英語'

    mocker.patch('app.handlers.update_memo.update_memo', side_effect=Exception('boom'))
    mocker.patch('app.services.translation_service.GoogleTranslator.convert', return_value='this is text')

    event = {
        'id': dummy_id,
        'body': {
            'text': text_origin,
            'origin_lang': origin_lang_name,
            'trans_lang': trans_lang_name
        }
    }
    
    response = lambda_handler(event, None)

    assert response.get('statusCode') == 500
    assert 'サーバーエラーが起きました。' in response.get('message')


# 翻訳が行えなかった場合
def test_translation_error(mocker):
    dummy_id = 'テスト1111'
    text_origin = 'テキストだよ'
    origin_lang_name = '日本語'
    trans_lang_name = '英語'

    dummy_update_result = {
        "statusCode": 200,
        "message": f"id:{dummy_id} のデータを書き換えました。"
    }

    mocker.patch('app.handlers.update_memo.update_memo', return_value=dummy_update_result)
    mocker.patch('app.services.translation_service.GoogleTranslator.convert', return_value=None)

    event = {
        'id': dummy_id,
        'body': {
            'text': text_origin,
            'origin_lang': origin_lang_name,
            'trans_lang': trans_lang_name
        }
    }
    
    response = lambda_handler(event, None)

    assert response.get('statusCode') == 400
    assert '翻訳が実行できませんでした。' in response.get('message')


# 渡された引数に正しくない形式があった場合
@pytest.mark.parametrize(
    ("dummy_id", "text_origin", "origin_lang_name", "trans_lang_name", "expected_status"),  # ← タプルとして記述！
    [
        ("", "テキストだよ", "日本語", "英語", 400),
        ("テスト1111", "", "日本語", "英語", 400),
        ("テスト1111", "テキストだよ", "", "英語", 400),
        ("テスト1111", "テキストだよ", "日本語", "", 400),
    ]
)
def test_bad_argument_error(mocker, dummy_id, text_origin, origin_lang_name, trans_lang_name, expected_status):
    dummy_update_result = {
        "statusCode": 200,
        "message": "id:テスト1111 のデータを書き換えました。"
    }

    mocker.patch('app.handlers.update_memo.update_memo', return_value=dummy_update_result)
    mocker.patch('app.services.translation_service.GoogleTranslator.convert', return_value='this is text')

    event = {
        'id': dummy_id,
        'body': {
            'text': text_origin,
            'origin_lang': origin_lang_name,
            'trans_lang': trans_lang_name
        }
    }
    
    response = lambda_handler(event, None)
    assert response['statusCode'] == expected_status