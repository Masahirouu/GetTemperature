import streamlit as st
from dotenv import load_dotenv
import os

st.title("Temperature!2")

load_dotenv()

api_key = os.getenv('API_KEY')
