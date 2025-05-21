# translation-memo

**translation-memo** は、指定した言語にメモを翻訳して登録・管理できるアプリケーションです。

## 前提条件
このアプリケーション起動には、ローカル環境に以下の環境が必要です
- python: 3.12

---

## セットアップ
1. リポジトリをクローンする
```bash
git clone git@github.com:oka-rena/translation-memo.git
```

2. リポジトリのディレクトリに移動する
```bash
cd translation-memo
```

3. venvで仮想環境を作る
```bash
python -m venv venv
```

4. 仮想環境をアクティブ化する
- windows
```bash
venv\Scripts\activate
```

- mac / linux
```bash
source venv/bin/activate
```

5. 必要なライブラリをインストールする
```bash
pip install -r requirements.txt
```

6. コードエディタでプロジェクトを開く (例: VSCodeなど)

---

# アプリケーションの使い方
## メモの登録
1. コードエディタで post.json を開き、以下のキーに適切な値を入力します。
```json
{
  "text": "メモの内容",
  "origin_lang": "元の言語",
  "trans_lang": "翻訳後の言語"
}
```

2. curlコマンドを実行して、メモを登録します。
```bash
curl -X POST -H "Content-Type: application/json" -d @post.json https://c7aq155hl3.execute-api.ap-northeast-1.amazonaws.com/transmemo-stage/post
```

## メモの取得
### メモのid一覧を取得する場合
1. 以下のコマンドを入力すると、メモの一覧が取得できます。（idはUUIDになっています）
```bash
curl -X GET https://c7aq155hl3.execute-api.ap-northeast-1.amazonaws.com/transmemo-stage
```

### 特定のメモの中味を取得する場合
1. idを指定して、GETリクエストを送ります。(id=の後ろにメモのUUIDを指定してください)
```bash
curl -X GET https://c7aq155hl3.execute-api.ap-northeast-1.amazonaws.com/transmemo-stage?id=idを入れる
```

## メモの更新
1. コードエディタで post.json を開きます。
「text」にメモを書き、「origin_lang」にメモを書いた言語、「trans_lang」に翻訳後の言語を記入してください。

2. curlコマンドを実行して、メモを更新します。(id=の後ろにメモのUUIDを指定してください)
```bash
curl -X PUT -H "Content-Type: application/json" -d @post.json https://c7aq155hl3.execute-api.ap-northeast-1.amazonaws.com/transmemo-stage?id=idを入れる
```

## メモの削除
1. idを指定して、メモを削除します。(id=の後ろにメモのUUIDを指定してください)
```bash
curl -X DELETE https://c7aq155hl3.execute-api.ap-northeast-1.amazonaws.com/transmemo-stage?id=idを入れる
```

---

## 備考
- このアプリケーションは、python・pytest・AWS Lambda の学習を目的として作成しました。
- AWS API Gateway を利用して、バックエンドと通信しています。
- app/handlers、app/service 内にあるコードを、AWS Lambdaで使用しています。