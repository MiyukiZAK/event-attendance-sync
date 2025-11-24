from playwright.sync_api import sync_playwright
import time
import os
from dotenv import load_dotenv

# ==============================
#   設定
# ==============================
load_dotenv()

EMAIL = os.getenv("TECHPLAY_EMAIL")
PASSWORD = os.getenv("TECHPLAY_PASSWORD")

DOWNLOAD_DIR = "/Users/miyukio/Downloads/techplay"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# TechPlay の出欠ページ URL テンプレ
EVENT_URL_TEMPLATE = "https://owner.techplay.jp/event/{event_id}/attendee"

# スプシ連携前のローカルテスト用
event_map = [
    ["989236", "T1209AI設計開発"],
    ["988538", "T1203個人開発"],
    ["989007", "T1204GLOBISコードレビュー"],
    ["988250", "T1120AIレビュー"],
]


# ==============================
# TechPlay CSV ダウンロード処理
# ==============================
def download_csv(event_id):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        # 出欠ページへアクセス → ログイン画面へリダイレクトされる
        print("\n🔐 出欠ページへアクセス → 自動リダイレクトを待つ…")
        page.goto(EVENT_URL_TEMPLATE.format(event_id=event_id))

        print("📩 メール入力")
        page.wait_for_selector("input[name='email']", timeout=30000)
        page.fill("input[name='email']", EMAIL)

        print("🔑 パスワード入力")
        page.fill("input[name='password']", PASSWORD)

        print("➡ ログイン実行")
        page.click("input[type='submit']")

        # ログイン後、出欠ページに戻るまで待機
        print("📄 CSV リンク確認中…")
        page.wait_for_selector("text=CSVダウンロード", timeout=30000)

        # ダウンロード
        print("⬇ CSVダウンロード開始")
        with page.expect_download() as download_info:
            page.click("text=CSVダウンロード")

        download = download_info.value

        # 🔥 ファイル名を event-attendee-{event_id}.csv に統一
        save_path = f"{DOWNLOAD_DIR}/event-attendee-{event_id}.csv"
        download.save_as(save_path)

        print(f"🎉 保存完了 → {save_path}")

        browser.close()
        return save_path


# ==============================
# メイン処理
# ==============================
def main():
    print("🚀 TechPlay CSV ダウンロード開始！\n")

    for event_id, sheet_name in event_map:
        print(f"\n===== TechPlay {event_id} : {sheet_name} =====")
        path = download_csv(event_id)

        if path:
            print(f"🎉 ダウンロード成功: {path}")
        else:
            print("❌ ダウンロード失敗")

    print("\n🎉 すべての TechPlay CSV ダウンロード完了！")


if __name__ == "__main__":
    main()
