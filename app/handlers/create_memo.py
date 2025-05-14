import json
from app.services.storage_service import save_memo
from app.services.translation_service import GoogleTranslator

def lambda_handler(event, context):
    try:
        body = event['body']
        text_origin = body.get('text')
        origin_lang_name = body.get('origin_lang')
        trans_lang_name = body.get('trans_lang')

        if not text_origin:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": f"入力テキスト:「{text_origin}」の取得に失敗しました。空文字などは登録できません。"
                }, ensure_ascii=False)
            }

        if not origin_lang_name:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": f"変換元の言語:「{origin_lang_name}」の取得に失敗しました。文字列で指定してください。"
                }, ensure_ascii=False)
            }
        
        if not trans_lang_name:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": f"変換先の言語:「{trans_lang_name}」の取得に失敗しました。文字列で指定してください。"
                }, ensure_ascii=False)
            }
        
        trans = GoogleTranslator()
        text_translated = trans.convert(text_origin, origin_lang_name, trans_lang_name) # 取得したテキストを翻訳
        if not text_translated:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "翻訳が実行できませんでした"
                }, ensure_ascii=False)
            }
        
        memo_id = save_memo(text_origin, text_translated) # 翻訳前と後のテキストをS3に送信
        if not memo_id:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "S3への保存ができませんでした"
                }, ensure_ascii=False)
            }

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "保存に成功しました",
                "id": memo_id,
                "translted": text_translated
            }, ensure_ascii=False)
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": f"サーバーエラーが発生しました - {e}"
            }, ensure_ascii=False)
        }