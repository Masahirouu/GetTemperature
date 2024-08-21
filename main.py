import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

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
        return None, None

    latest_data = rows[-1]  # 最新の行を取得
    return {
        "date": latest_data[0],
        "time": latest_data[1],
        "temperature": latest_data[2]
    }, rows

# Streamlitの表示
st.title("Room Temperature")

# get_latest_data関数からlatest_dataとrowsを取得
latest_data, rows = get_latest_data()

if latest_data:
    st.markdown(f"<span style='font-size:24px;'>Date: {latest_data['date']}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:24px;'>Time: {latest_data['time']}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:24px;'>Temperature: {latest_data['temperature']}°C</span>", unsafe_allow_html=True)
else:
    st.error("No data found.")
    
#####

if rows:
    # 最新のデータから72個分のデータを取得（約6時間分）
    data_to_plot = rows[-72:]

    # データをDataFrameに変換
    df = pd.DataFrame(data_to_plot, columns=["Date", "Time", "Temperature"])

    # 'Temperature'をfloatに変換
    df["Temperature"] = df["Temperature"].astype(float)

    # 'Date'と'Time'を結合してdatetime型に変換
    df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])

    # 折れ線グラフを作成
    plt.figure(figsize=(10, 5))
    plt.plot(df["Datetime"], df["Temperature"], marker="o", color="orange", label="Temperature (°C)")

    # 目印の線を追加
    plt.axhline(y=28, color="red", linestyle="--", label="Upper value (28°C)")
    plt.axhline(y=20, color="blue", linestyle="--", label="Lower value (20°C)")

    # グリッド線の追加
    plt.grid(True)

    # グラフのラベル設定
    plt.xlabel("Time", fontsize=12)  # フォントサイズを大きく設定
    plt.ylabel("Temperature (°C)", fontsize=12)  # フォントサイズを大きく設定
    plt.title("Temperature over the last 6 hours", fontsize=14)  # タイトルのフォントサイズを大きく設定

    # x軸のラベルを30分おきに設定し、書式をYYYY/MM/DD HH:MMに設定
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0, 30]))  # 00分と30分ごとにラベルを設定

    # ラベルを回転させて表示
    plt.xticks(rotation=45, ha="right", fontsize=10)  # x軸のフォントサイズを大きく設定
    plt.yticks(fontsize=10)  # y軸のフォントサイズを大きく設定

    # 凡例を追加
    plt.legend(loc="upper right", fontsize=10)

    # グラフの表示
    plt.tight_layout()  # レイアウトを調整
    st.pyplot(plt)
else:
    st.warning("No historical data available for plotting.")
