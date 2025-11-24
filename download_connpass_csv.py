import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =========================================
# 🎯 CSV を取得したい Connpass イベント一覧
# 追加・削除したければ、このリストを編集するだけ！
# =========================================
EVENT_LIST = [
    "371779", # 1127PdM
    "374188", # 1203個人開発
    "374875", # 1204GLOBISコードレビュー
    "374877",   # 1209AI設計開発
    
]

# =========================================
# CSV 保存先
# =========================================
DOWNLOAD_DIR = os.path.expanduser("~/Downloads/connpass")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# =========================================
# Cookie 読み込み
# =========================================
def load_cookies(driver, path):
    with open(path, "r") as f:
        cookies = json.load(f)

    cleaned = []

    for cookie in cookies:
        cookie["domain"] = "connpass.com"

        if "sameSite" in cookie:
            if cookie["sameSite"] not in ["Strict", "Lax", "None"]:
                cookie["sameSite"] = "Lax"

        if "expiry" in cookie and isinstance(cookie["expiry"], str):
            try:
                cookie["expiry"] = int(cookie["expiry"])
            except:
                cookie.pop("expiry", None)

        cleaned.append(cookie)

    for cookie in cleaned:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print("SKIP:", cookie, "理由:", e)

# =========================================
# メイン処理
# =========================================
def main():
    options = Options()
    # options.add_argument("--headless=new")

    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": DOWNLOAD_DIR,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "safebrowsing.disable_download_protection": True,
        },
    )

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        # Cookie適用のためトップページを開く
        driver.get("https://connpass.com/")
        time.sleep(2)

        # Cookie読み込み
        load_cookies(driver, "cookies.json")

        # ======= イベントを1つずつ処理する =======
        for event_id in EVENT_LIST:
            print(f"\n=== 📥 {event_id} のCSVをダウンロード中 ===")

            event_url = f"https://connpass.com/event/{event_id}/participants/?d=1"
            driver.get(event_url)

            csv_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@href, 'participants_csv')]")
                )
            )

            driver.execute_script("arguments[0].click();", csv_button)
            time.sleep(6)

            print(f"✔ ダウンロード完了: {event_id}")

        print("\n🎉 すべてのCSVダウンロード完了！ →", DOWNLOAD_DIR)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
