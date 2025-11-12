import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- 페이지 설정 ---
st.set_page_config(
    page_title="🌍 MBTI by Country",
    page_icon="🌱",
    layout="wide"
)

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()
countries = df["Country"].unique()
mbti_types = [c for c in df.columns if c != "Country"]

#
