import json
from app.services.storage_service import delete_memo

def lambda_handler(event, context):
    query_id = event.get('id', None)
    if not query_id:
        response = json.dumps({
            "statusCode": 400,
            "message": "error!: データが見つかりませんでした"
        }, ensure_ascii=False)
        return json.loads(response)
    
    return json.loads(delete_memo(query_id))