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
        Body=json.dumps(data, ensure_ascii=False)
    )
    return memo_id


def get_memo(memo_id:str =''):
    """
    条件に則したメモの内容（辞書型） or 一覧（リスト型）を返す
    """
    s3 = boto3.client('s3')
    bucket_name = 'translation-memo'
    folder_prefix = 'memos'
    file_key = f'{folder_prefix}/{memo_id}.json'

    if not memo_id:
        response = s3.list_objects_v2(
            Bucket=bucket_name,
            Prefix=folder_prefix
        )
        # 文字列の形成（['テストテスト1111', 'サンプルデータ2222']のように取得できるように）
        files = [obj['Key'].replace('memos/', '').replace('.json', '') for obj in response.get('Contents', [])]
        return files if 'Contents' in response else None

    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        return json.loads(response['Body'].read().decode('utf-8'))
    except s3.exceptions.NoSuchKey:
        return None 


def update_memo(memo_id:str, original: str, translated: str):
    s3 = boto3.client('s3')
    bucket_name = 'translation-memo'
    folder_prefix = 'memos'
    file_key = f'{folder_prefix}/{memo_id}.json'

    try:
        s3.get_object(Bucket=bucket_name, Key=file_key)
    except Exception as e:
        return {
            "statusCode": 500,
            "message": f"error! データが見つかりません。 - {e}"
        }

    data = {
        'id': memo_id,
        'original': original,
        'translated': translated
    }
    try:
        s3.put_object(
            Bucket='translation-memo',
            Key=f'memos/{memo_id}.json',
            Body=json.dumps(data, ensure_ascii=False)
        )
        return {
            "statusCode": 200,
            "message": f"id:{memo_id} のデータを書き換えました。"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "message": f"error! データの書き換えに失敗しました。 - {e}"
        }


def delete_memo(memo_id:str):
    BUCKET_NAME = 'translation-memo'
    DELETE_DIR_PATH = 'memos'
    FILE_NAME = f'{memo_id}.json'
    s3 = boto3.client('s3')
    delete_file_path = f'{DELETE_DIR_PATH}/{FILE_NAME}'

    # ファイルが存在するか確認（s3はオブジェクトがなくても、削除成功をかえしてしまうため）
    try:
        s3.head_object(Bucket=BUCKET_NAME, Key=delete_file_path)
    except s3.exceptions.ClientError:
        return json.dumps({
            "statusCode": 500,
            "message": "error!: 削除対象のデータが存在しません。"
        }, ensure_ascii=False)

    # データの削除
    try:
        response = s3.delete_object(Bucket=BUCKET_NAME, Key=delete_file_path)
        print(response)
        return json.dumps({
            "statusCode": 200,
            "message": "データの削除が完了しました"
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({
            "statusCode": 500,
            "message": f"error!: データを削除できませんでした。 - {e}"
        }, ensure_ascii=False)