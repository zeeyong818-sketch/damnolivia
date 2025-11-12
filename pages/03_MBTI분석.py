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
fig = px.bar(
    country_data,
    x=country_data.index,
    y="비율",
    color=country_data.index,
    color_discrete_sequence=colors,
    title=f"🇨🇮 {selected_country}의 MBTI 분포",
)

fig.update_layout(
    showlegend=False,
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    plot_bgcolor="white",
    paper_bgcolor="white",
    title_x=0.5,
    font=dict(size=15),
)
fig.update_traces(
    hovertemplate="<b>%{x}</b><br>비율: %{y:.2%}<extra></extra>"
)

# --- 그래프 표시 ---
st.plotly_chart(fig, use_container_width=True)

# --- 요약 ---
st.subheader("📊 요약")
st.write(f"이 나라에서 가장 많은 유형은 **{top_type}** 입니다 💫")
