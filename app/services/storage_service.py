# 翻訳結果をS3へ保存する機能の提供
import uuid
import json
import boto3

def save_memo(original: str, translated: str) -> str:
    """
    翻訳メモを保存して、IDを返す
    """
    s3 = boto3.client('s3')
    memo_id = str(uuid.uuid4())
    data = {
        'id': memo_id,
        'original': original,
        'translated': translated
    }
    s3.put_object(
        Bucket='translation-memo',
        Key=f'memos/{memo_id}.json',
        Body=json.dumps(data)
    )
    return memo_id