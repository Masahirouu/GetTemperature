import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import os
# print("stop")
# quit()

# load_dotenv()
# api_key = os.getenv('API_KEY')

# Google Sheets APIの認証
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("key.json", scope)
client = gspread.authorize(creds)

# Googleスプレッドシートにアクセス
spreadsheet_id = "1EaxGSeCzjFUqwXGU3w_hEiTSHaZWNSY78UdNc3-j9b8"
worksheet_name = "1"  # シート名を指定

@st.cache_data(ttl=300)  # キャッシュの有効期限を5分（300秒）に設定
def get_latest_data():
    sheet = client.open_by_key(spreadsheet_id).worksheet(worksheet_name)
    rows = sheet.get_all_values()

    if not rows:
        return None

    latest_data = rows[-1]  # 最新の行を取得
    return {
        "date": latest_data[0],
        "time": latest_data[1],
        "temperature": latest_data[2]
    }

# Streamlitの表示
st.title("Observed Temperature")

latest_data = get_latest_data()
if latest_data:
    st.write(f"Date: {latest_data['date']}")
    st.write(f"Time: {latest_data['time']}")
    st.write(f"Temperature: {latest_data['temperature']}°C")
else:
    st.error("No data found.")