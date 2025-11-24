import os
import glob
import csv
import gspread
from google.oauth2.service_account import Credentials

# ============================================
#  文字コードを自動判別して CSV を読み込む関数
# ============================================
def read_csv_auto(csv_path):
    encodings = ["utf-8", "utf-8-sig", "cp932", "shift_jis"]

    for enc in encodings:
        try:
            with open(csv_path, newline="", encoding=enc) as f:
                return list(csv.reader(f))
        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError(f"❌ CSV の文字コードを判定できません: {csv_path}")

# ============================================
#  CSV → シートへ上書きする関数
# ============================================
def upload_csv_to_sheet(sheet, csv_path):
    print(f"📄 読み込み中: {csv_path}")

    rows = read_csv_auto(csv_path)

    sheet.clear()
    sheet.update("A1", rows)

    print(f"✨ 更新完了！ → {sheet.title}")

# ============================================
#  メイン処理
# ============================================
def main():
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(creds)

    ss = client.open_by_key("1Vxw0rLa8vzljI2RggM68oIfLQjBHzhDHJqNfsKnzLMY")
    map_sheet = ss.worksheet("event_map")

    data = map_sheet.get_all_values()[1:]

    download_base = "/Users/miyukio/Downloads"

    print("🚀 すべての CSV → スプレッドシート更新を開始します！\n")

    for row in data:
        event_id, platform, sheet_name = row

        if not event_id:
            continue

        try:
            sheet = ss.worksheet(sheet_name)
        except:
            print(f"❌ シートが見つかりません: {sheet_name}")
            continue

        # ===============================
        #   CSV ファイルのパス設定
        # ===============================
        if platform == "connpass":
            folder = os.path.join(download_base, "connpass")
            csv_pattern = f"{folder}/event_{event_id}_participants*.csv"

        elif platform == "techplay":
            folder = os.path.join(download_base, "techplay")
            csv_pattern = f"{folder}/event-attendee-{event_id}*.csv"

        else:
            print(f"❌ 不明なプラットフォーム: {platform}")
            continue

        # ===============================
        #   最新 CSV を取得
        # ===============================
        csv_files = glob.glob(csv_pattern)

        if not csv_files:
            print(f"❌ CSV が見つかりません: {csv_pattern}")
            continue

        csv_path = max(csv_files, key=os.path.getmtime)

        print(f"➡️ 最新 CSV を使用: {csv_path}")

        try:
            upload_csv_to_sheet(sheet, csv_path)
        except Exception as e:
            print(f"❌ アップロードエラー（{sheet_name}）: {e}")

    print("\n🎉 すべての CSV → スプレッドシート更新が完了しました！")

if __name__ == "__main__":
    main()
