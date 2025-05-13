# services/storage_service.py のテスト
import boto3
import json
from moto import mock_aws
from app.services.storage_service import save_memo

@mock_aws
def test_save_memo():
    # モックでS3バケットを再現
    s3 = boto3.client('s3')
    bucket_name = 'translation-memo'
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-1'})

    origin_text = "こんにちは"
    translated_text = "Hello"

    memo_id = save_memo(origin_text, translated_text)

    # S3から保存されたオブジェクトを取得して検証
    response = s3.get_object(
        Bucket=bucket_name,
        Key=f'memos/{memo_id}.json',
    )
    content = json.load(response['Body'])
    print(content)

    assert content['id'] == memo_id
    assert content['original'] == origin_text
    assert content['translated'] == translated_text