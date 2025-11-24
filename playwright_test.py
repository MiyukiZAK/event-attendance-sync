from playwright.sync_api import sync_playwright
import time
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("TP_EMAIL")
PASSWORD = os.getenv("TP_PASSWORD")

EVENT_ID = "989236"  # まずは 1件で検証

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print("🔐 出欠ページへアクセス → 自動リダイレクトを待つ…")
        page.goto(f"https://owner.techplay.jp/event/{EVENT_ID}/attendee")

        # ログインページが出るまで待つ
        page.wait_for_selector("input[name='email']", timeout=30000)

        print("📩 メール入力")
        page.fill("input[name='email']", EMAIL)

        print("🔑 パスワード入力")
        page.fill("input[name='password']", PASSWORD)

        print("➡ ログイン実行")
        # ★修正ポイント★ button ではなく input[type=submit]
        page.click("input[type='submit']")

        # ページ遷移（ログイン → 出欠ページ）が終わるのを待つ
        page.wait_for_load_state("networkidle")

        print("📄 CSV リンク確認中…")
        page.wait_for_selector("text=CSVダウンロード", timeout=30000)

        print("⬇ CSVダウンロード開始")
        with page.expect_download() as download_info:
            page.click("text=CSVダウンロード")
        download = download_info.value
        download.save_as(f"./techplay_latest.csv")

        print("🎉 完了！ techplay_latest.csv に保存しました")

        browser.close()

if __name__ == "__main__":
    main()
