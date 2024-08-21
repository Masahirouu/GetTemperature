import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

# 環境変数の取得
private_key = os.getenv("PRIVATE_KEY").replace('\\n', '\n')  # 改行文字の修正
credentials_dict = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": private_key,
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL")
}

# Google Sheets APIの認証
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
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
    st.markdown(f"<span style='font-size:24px;'>Date: {latest_data['date']}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:24px;'>Time: {latest_data['time']}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:24px;'>Temperature: {latest_data['temperature']}°C</span>", unsafe_allow_html=True)
else:
    st.error("No data found.")