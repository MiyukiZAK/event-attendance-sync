# master_run.py
import subprocess
import traceback
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO   = os.getenv("EMAIL_TO")


# -----------------------------------------
#  メール送信関数
# -----------------------------------------
def send_mail(subject, body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
        print("📧 メール送信成功！")
    except Exception as e:
        print("❌ メール送信エラー:", e)


# -----------------------------------------
#  スクリプト実行
# -----------------------------------------
def run_script(name, cmd):
    print(f"\n===== {name} =====")
    try:
        result = subprocess.run(
            ["python3", cmd],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True, result.stdout
    except Exception as e:
        print(f"❌ {name} エラー: {e}")
        print(traceback.format_exc())
        return False, str(e)


# -----------------------------------------
#  メイン処理
# -----------------------------------------
def main():
    messages = []
    all_ok = True

    # 1) connpass ダウンロード
    ok, msg = run_script("Connpass DL", "download_connpass_csv.py")
    messages.append(f"Connpass: {'OK' if ok else 'NG'}")
    if not ok: all_ok = False

    # 2) TechPlay ダウンロード
    ok, msg = run_script("TechPlay DL", "download_techplay_csv.py")
    messages.append(f"TechPlay: {'OK' if ok else 'NG'}")
    if not ok: all_ok = False

    # 3) Sheets へアップロード
    ok, msg = run_script("Upload CSV to Sheets", "upload_csv_auto.py")
    messages.append(f"Upload: {'OK' if ok else 'NG'}")
    if not ok: all_ok = False

    # メール本文生成
    subject = "【自動処理完了】Connpass/TechPlay → スプレッドシート反映"
    body = "\n".join(messages)

    # メール送信
    send_mail(subject, body)

    print("\n===== 全処理完了 =====")
    print(body)


if __name__ == "__main__":
    main()
