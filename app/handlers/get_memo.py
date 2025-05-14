import json
from app.services.storage_service import get_memo

def lambda_handler(event, context):
    # if(idクエリパラムありかなしか)
    # あり：bodyをdumpsで直接返す　なし：memo_idのリストを返す
    query_id = event.get('id')
    if query_id:
        data = get_memo(query_id)
        if not data:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "データが取得できませんでした"
                }, ensure_ascii=False)
            }
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "メモの内容を表示します",
                "data": data
            }, ensure_ascii=False)
        }
    else:
        data = get_memo()

        if data == []:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "データが空です"
                }, ensure_ascii=False)
            }
        if data is None:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "データが取得できませんでした"
                }, ensure_ascii=False)
            }
        
        id_list = []
        for d in data:
            id_list.append(d)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "メモのid一覧を表示します",
                "data": id_list
            }, ensure_ascii=False)
        }
