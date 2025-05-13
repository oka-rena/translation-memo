import json
from app.services.storage_service import save_memo
from app.services.translation_service import GoogleTranslator

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", {}))
        text_origin = body.get('text')
        trans_lang_name = body.get('trans_lang')

        if not text_origin:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": f"入力テキスト:「{text_origin}」の取得に失敗しました。空文字などは登録できません。"
                })
            }
        
        if not trans_lang_name:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": f"変換先の言語:「{trans_lang_name}」の取得に失敗しました。文字列で指定してください。"
                })
            }
        
        text_translated = GoogleTranslator.convert(text_origin, trans_lang_name) # 取得したテキストを翻訳
        memo_id = save_memo(text_origin, text_translated) # 翻訳前と後のテキストをS3に送信

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "保存に成功しました",
                "id": memo_id,
                "translted": text_translated
            })
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": f"サーバーエラーが発生しました - {e}"
            })
        }