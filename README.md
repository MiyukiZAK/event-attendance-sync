# event-attendance-sync

connpass / TechPlay の参加者 CSV を自動ダウンロードし、Google スプレッドシートへ反映するバッチ処理です。  
Mac の `cron` を使って **毎朝8時 / 毎夕18時半に完全自動実行**できます。

---

## 🚀 機能一覧

- connpass の参加者 CSV を Selenium + Cookie ログインで自動ダウンロード
- TechPlay の参加者 CSV を Playwright で自動ダウンロード
- 最新 CSV を Google スプレッドシートに上書きアップロード
- 実行結果をメール通知（成功・失敗を1通に）

---

## 🧱 ディレクトリ構成

event-attendance-sync/
├── download_connpass_csv.py
├── download_techplay_csv.py
├── upload_csv_auto.py
├── master_run.py # 「ダウンロード → アップロード → メール送信」一括実行
├── cookies.json
├── cookies_techplay.json
├── credentials.json # Google service account 認証
├── .env # メール情報 & TechPlay ログイン情報
└── README.md

yaml
Copy code

---

## 🔧 必要なもの

### 1. Python 3.13
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3

yaml
Copy code

### 2. Google Service Account の credentials.json  
スプレッドシートへの編集権限が必要。

### 3. connpass / TechPlay の Cookie  
ログイン状態を維持して CSV を取得するために必要。

---

## 🔑 `.env` の書き方

メール送信用
SMTP_USER=xxxx
SMTP_PASS=xxxx

TechPlay ログイン
TP_EMAIL=xxxx
TP_PASSWORD=xxxx

yaml
Copy code

---

## 📝 イベントの追加・削除の方法

### 🔹 **connpass の場合**
`download_connpass_csv.py` の冒頭を編集します。

```python
EVENT_LIST = [
    "374877",   # 1209AI設計開発
    "374875",   # 1204GLOBISコードレビュー
]
イベント URL の番号（例: https://connpass.com/event/374877/ → 374877）を追加するだけ。

🔹 TechPlay の場合
download_techplay_csv.py の冒頭を編集します。

python
Copy code
event_map = [
    ["989236", "T1209AI設計開発"],
    ["989007", "T1204GLOBISコードレビュー"],
]
[イベントID, シート名] を追加するだけです。

▶ 一括実行
すべての処理はこれだけでOK：

nginx
Copy code
python3 master_run.py
connpass DL

TechPlay DL

スプレッドシート更新

実行報告メール送信

⏱ 自動実行（cron）
cron を編集
nginx
Copy code
crontab -e
毎朝8時 & 毎夕18時半に実行する設定
swift
Copy code
0 8 * * * /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 /Users/miyukio/Desktop/event-attendance-sync/master_run.py
30 18 * * * /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 /Users/miyukio/Desktop/event-attendance-sync/master_run.py
🛑 セキュリティについて
このリポジトリは 必ず Private（非公開） としてください。
以下のファイルは機密情報です：

.env

cookies.json

cookies_techplay.json

credentials.json

