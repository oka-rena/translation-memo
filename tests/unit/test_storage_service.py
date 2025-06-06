# services/storage_service.py のテスト
import boto3
import json
import pytest
from moto import mock_aws
from app.services.storage_service import save_memo, get_memo, update_memo, delete_memo

@pytest.fixture
def setup():
    """
    S3バケットの再現処理を共通化
    """
    with mock_aws():
        s3 = boto3.client('s3')
        bucket_name = 'translation-memo'
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-1'})

        origin_text = "こんにちは"
        translated_text = "Hello"

        try:
            yield s3, bucket_name, origin_text, translated_text
        finally:
            # バケット内のオブジェクトをすべて削除
            response = s3.list_objects_v2(Bucket=bucket_name)
            if "Contents" in response:
                for obj in response["Contents"]:
                    s3.delete_object(Bucket=bucket_name, Key=obj["Key"])

            # バケットを削除
            s3.delete_bucket(Bucket=bucket_name)


# save_memoメソッドのテスト
class TestSaveMemo():
    # S3への登録に成功する
    def test_save_memo_success(self, setup):
        s3, bucket_name, origin_text, translated_text  = setup

        # メモをS3に登録する処理
        memo_id = save_memo(origin_text, translated_text)

        # S3から保存されたオブジェクトを取得してidの検証
        response = s3.get_object(
            Bucket=bucket_name,
            Key=f'memos/{memo_id}.json',
        )
        content = json.load(response['Body'])

        assert content['id'] == memo_id


# get_memoメソッドのテスト
class TestGetMemo():
    # 正常処理
    # idが渡されたとき（単一のデータが返される）
    def test_get_memo_success(self, setup):
        s3, bucket_name, origin_text, translated_text  = setup
        dummy_memo_id = 'テストテスト1111'

        # ダミー情報を登録
        body_content = {"id": dummy_memo_id, "original": origin_text, "translated": translated_text}
        s3.put_object(
            Bucket=bucket_name,
            Key=f'memos/{dummy_memo_id}.json',
            Body=json.dumps(body_content, ensure_ascii=False)
        )

        # 保存されたs3を取得する
        memo = get_memo(dummy_memo_id)
        assert memo == body_content
        assert isinstance(memo, dict)


    # idが渡らなかったとき（一覧が取得できる）
    def test_get_memo_list_success(self, setup):
        print(setup)
        s3, bucket_name, origin_text, translated_text  = setup
        dummy_memo_ids = ['テストテスト1111', 'テストダミー222', 'testtdata3333']

        # ダミー情報を登録
        for memo_id in dummy_memo_ids:
            body_content = {"id": memo_id, "original": origin_text, "translated": translated_text}
            s3.put_object(
                Bucket=bucket_name,
                Key=f'memos/{memo_id}.json',
                Body=json.dumps(body_content, ensure_ascii=False)
            )

        # 保存されたs3を取得する
        memo = get_memo('')
        assert set(memo) == set(dummy_memo_ids)
        assert isinstance(memo, list)


    # 例外処理
    # 存在しないメモを取得する（単一データ）
    def test_get_memo_not_found(self, setup):
        s3, bucket_name, origin_text, translated_text  = setup
        dummy_memo_id = 'テストテスト1111'
        non_existent_memo_id = "not_exist_9999"

        # ダミー情報を登録
        body_content = {"id": dummy_memo_id, "original": origin_text, "translated": translated_text}
        s3.put_object(
            Bucket=bucket_name,
            Key=f'memos/{dummy_memo_id}.json',
            Body=json.dumps(body_content, ensure_ascii=False)
        )

        memo = get_memo(non_existent_memo_id)
        assert memo is None


    # 存在しないメモを取得する（リストデータ）
    def test_get_memo_list_not_found(self, setup):
        s3, bucket_name, origin_text, translated_text  = setup
        dummy_memo_id = 'テストテスト1111'
        non_existent_memo_id = "not_exist_9999"

        # ダミー情報を登録
        body_content = {"id": dummy_memo_id, "original": origin_text, "translated": translated_text}
        s3.put_object(
            Bucket=bucket_name,
            Key=f'memos/{dummy_memo_id}.json',
            Body=json.dumps(body_content, ensure_ascii=False)
        )

        memo = get_memo(non_existent_memo_id)
        assert memo is None


class TestUpdateMemo():
    # 正常処理
    def test_update_success(self, setup):
        s3, bucket_name, origin_text, translated_text  = setup
        dummy_memo_id = 'テストテスト1111'
        update_origin = 'データを更新します'
        update_trans = 'this data is updated'

        # ダミー情報を登録
        body_content = {"id": dummy_memo_id, "original": origin_text, "translated": translated_text}
        s3.put_object(
            Bucket=bucket_name,
            Key=f'memos/{dummy_memo_id}.json',
            Body=json.dumps(body_content, ensure_ascii=False)
        )

        # データを更新
        response = update_memo(dummy_memo_id, update_origin, update_trans)

        # 更新後のデータを確認
        get_file = s3.get_object(
            Bucket=bucket_name,
            Key=f'memos/{dummy_memo_id}.json',
        )
        file_content = get_file['Body'].read().decode("utf-8")
        file_content = json.loads(file_content)

        assert response.get('statusCode') == 200
        assert response.get('message') == f'id:{dummy_memo_id} のデータを書き換えました。'

        assert file_content.get('id') == dummy_memo_id
        assert file_content.get('original') == update_origin
        assert file_content.get('translated') == update_trans


    # 例外処理
    # 登録されているデータがない場合
    def test_update_data_not_found(self, setup):
        s3, bucket_name, origin_text, translated_text  = setup
        dummy_memo_id = 'テストテスト1111'
        update_origin = 'データを更新します'
        update_trans = 'this data is updated'
        
        # データを登録しない状態で更新
        response = update_memo(dummy_memo_id, update_origin, update_trans)

        assert response.get('statusCode') == 500
        assert 'error! データが見つかりません。' in response.get('message')


    # 更新中にサーバーエラーが発生した場合
    def test_update_data_exception(self, setup, mocker):
        s3, bucket_name, origin_text, translated_text  = setup
        # ダミーデータを登録
        dummy_memo_id = 'テストテスト1111'
        update_origin = 'データを更新します'
        update_trans = 'this data is updated'
        body_content = {"id": dummy_memo_id, "original": origin_text, "translated": translated_text}
        
        s3.put_object(
            Bucket=bucket_name,
            Key=f'memos/{dummy_memo_id}.json',
            Body=json.dumps(body_content, ensure_ascii=False)
        )

        # サーバーエラーを起こすモック
        mock_s3 = mocker.patch("boto3.client")
        mock_s3.return_value.put_object.side_effect = Exception("boom")
        response = update_memo(dummy_memo_id, update_origin, update_trans)

        assert response.get('statusCode') == 500
        assert 'error! データの書き換えに失敗しました。' in response.get('message')


# delete_memoメソッドのテスト
class TestDeleteMemo():
    # 正常処理
    def test_delete_memo_success(self, setup):
        s3, bucket_name, origin_text, translated_text  = setup
        folder_prefix = 'memos'
        dummy_memo_ids = ['テストテスト1111', 'テストダミー222', 'testtdata3333']
        delete_target_id = 'テストテスト1111'

        # ダミー情報を登録
        for memo_id in dummy_memo_ids:
            body_content = {"id": memo_id, "original": origin_text, "translated": translated_text}
            s3.put_object(
                Bucket=bucket_name,
                Key=f'memos/{memo_id}.json',
                Body=json.dumps(body_content, ensure_ascii=False)
            )
        
        # 削除する
        delete_response = delete_memo(delete_target_id)
        result = json.loads(delete_response)

        # 保存されたオブジェクトを取得して残りの検証
        get_response = s3.list_objects_v2(
            Bucket=bucket_name,
            Prefix=folder_prefix
        )
        list_data = [obj['Key'] for obj in get_response.get('Contents')]

        assert result['statusCode'] == 200
        assert result['message'] == "データの削除が完了しました"
        assert len(list_data) == 2
        print(list_data)


    # 例外処理
    # 削除対象削除対象のidが未指定の場合
    def test_delete_memo_not_id(self, setup):
        s3, bucket_name, origin_text, translated_text  = setup
        dummy_memo_ids = ['テストテスト1111', 'テストダミー222', 'testtdata3333']
        delete_target_id = ''

        # ダミー情報を登録
        for memo_id in dummy_memo_ids:
            body_content = {"id": memo_id, "original": origin_text, "translated": translated_text}
            s3.put_object(
                Bucket=bucket_name,
                Key=f'memos/{memo_id}.json',
                Body=json.dumps(body_content, ensure_ascii=False)
            )
        
        # 削除する
        delete_response = delete_memo(delete_target_id)
        result = json.loads(delete_response)

        assert result['statusCode'] == 400
        assert result['message'] == "error!: データが見つかりませんでした"


    # 指定されたidのデータが見つからなかった場合
    def test_delete_memo_not_found(self, setup):
        s3, bucket_name, origin_text, translated_text  = setup
        dummy_memo_ids = ['テストテスト1111', 'テストダミー222', 'testtdata3333']
        delete_target_id = 'エラーid-4444'

        # ダミー情報を登録
        for memo_id in dummy_memo_ids:
            body_content = {"id": memo_id, "original": origin_text, "translated": translated_text}
            s3.put_object(
                Bucket=bucket_name,
                Key=f'memos/{memo_id}.json',
                Body=json.dumps(body_content, ensure_ascii=False)
            )
        
        # 削除する
        delete_response = delete_memo(delete_target_id)
        result = json.loads(delete_response)

        assert result['statusCode'] == 500
        assert result['message'] == "error!: 削除対象のデータが存在しません。"


    # Exceptionエラーが発生した場合
    def test_delete_memo_exception(self, mocker):
        mock_s3 = mocker.patch("boto3.client")
        mock_s3.return_value.delete_object.side_effect = Exception("boom")

        result = json.loads(delete_memo("test-id"))
        
        assert result["statusCode"] == 500
        assert "error!: データを削除できませんでした" in result["message"]
