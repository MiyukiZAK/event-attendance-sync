import gspread

gc = gspread.service_account(filename="credentials.json")
sh = gc.open_by_key("1Vxw0rLa8vzljI2RggM68oIfLQjBHzhDHJqNfsKnzLMY")
ws = sh.worksheet("event_map")

print(ws.get_all_values())
