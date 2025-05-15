import json
from app.services.translation_service import GoogleTranslator
from app.services.storage_service import update_memo

def lambda_handler(event, context):
    try:
        query_id = event['id']
        if not query_id:
            return {
                'statusCode': 400,
                'message': 'idが指定されていません。'
            }
        
        request_body = json.loads(json.dumps(event['body'], ensure_ascii=False))
        text_origin = request_body.get('text', None)
        origin_lang_name = request_body.get('origin_lang', None)
        trans_lang_name = request_body.get('trans_lang', None)

        if not text_origin:
            return {
                "statusCode": 400,
                "message": f"入力テキスト:「{text_origin}」の取得に失敗しました。空文字などは登録できません。"
            }

        if not origin_lang_name:
            return {
                "statusCode": 400,
                "message": f"変換元の言語:「{origin_lang_name}」の取得に失敗しました。文字列で指定してください。"
            }
        
        if not trans_lang_name:
            return {
                "statusCode": 400,
                "message": f"変換先の言語:「{trans_lang_name}」の取得に失敗しました。文字列で指定してください。"
            }
        
        trans = GoogleTranslator()
        text_translated = trans.convert(text_origin, origin_lang_name, trans_lang_name) # 取得したテキストを翻訳
        if not text_translated:
            return {
                "statusCode": 400,
                "message": "翻訳が実行できませんでした。"
            }
        
        return update_memo(query_id, text_origin, text_translated)
    except Exception as e:
        return {
            'statusCode':500,
            'message': f"サーバーエラーが起きました。 - {e}"
        }