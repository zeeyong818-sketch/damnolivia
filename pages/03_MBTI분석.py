import streamlit as st
import pandas as pd
import plotly.express as px

# --- 페이지 기본 설정 ---
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

# --- 제목 ---
st.title("🌍 국가별 MBTI 분포 시각화")
st.markdown("각 나라에서 MBTI 유형이 얼마나 분포하는지 확인해보세요!")

# --- 국가 선택 ---
selected_country = st.selectbox("국가를 선택하세요:", sorted(countries))

# --- 선택한 나라 데이터 처리 ---
country_data = df[df["Country"] == selected_country].drop(columns=["Country"]).T
country_data.columns = ["비율"]
country_data = country_data.sort_values("비율", ascending=False)
top_type = country_data.index[0]

# --- 색상 설정 ---
colors = ["#90e0ef"] * len(country_data)
colors[0] = "#00c853"  # 1등 초록색

# --- 그래프 생성 ---
fi
