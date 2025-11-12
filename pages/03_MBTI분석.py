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

# --- 제목 ---
st.title("🌍 국가별 MBTI 데이터 시각화 대시보드")
st.markdown("Plotly로 인터랙티브하게 MBTI 데이터를 살펴보세요 💫")

# --- 탭 구성 ---
tab1, tab2 = st.tabs(["📊 국가별 MBTI 비율", "🌐 MBTI 유형별 상위 국가"])

# ---------------------------------------------------------------------
# ✅ 탭 1: 국가별 MBTI 비율
# ---------------------------------------------------------------------
with tab1:
    st.subheader("📍 국가별 MBTI 분포 보기")
    selected_country = st.selectbox("국가를 선택하세요:", sorted(countries))

    # 해당 국가 데이터 정리
    country_data = df[df["Country"] == selected_country].drop(columns=["Country"]).T
    country_data.columns = ["비율"]
    country_data = country_data.sort_values("비율", ascending=False)
    top_type = country_data.index[0]

    # --- 색상 (파란색 그라데이션 반대 방향 + 1등 초록색) ---
    num = len(country_data)
    gradient = [f"rgba({50 + i*2}, {180 + i}, 255, 0.9)" for i in range(num)][::-1]  # 반대 그라데이션
    colors = gradient.copy()
    colors[country_data.index.get_loc(top_type)] = "#00c853"  # 1등 초록색

    # --- 그래프 ---
    fig1 = px.bar(
        country_data,
        x=country_data.index,
        y="비율",
        color=country_data.index,
        color_discrete_sequence=colors,
        title=f"🇨🇮 {selected_country}의 MBTI 분포",
    )

    fig1.update_layout(
        showlegend=False,
        xaxis_title="MBTI 유형",
        yaxis_title="비율",
        plot_bgcolor="white",
        paper_bgcolor="white",
        title_x=0.5,
        font=dict(size=15),
    )
    fig1.update_traces(hovertemplate="<b>%{x}</b><br>비율: %{y:.2%}<extra></extra>")
    st.plotly_chart(fig1, use_container_width=True)
    st.write(f"이 나라에서 가장 많은 유형은 **{top_type}** 입니다 💫")

# ---------------------------------------------------------------------
# ✅ 탭 2: MBTI 유형별 상위 국가
# ---------------------------------------------------------------------
with tab2:
    st.subheader("🌐 MBTI 유형별 상위 국가 보기")
    selected_type = st.selectbox("MBTI 유형을 선택하세요:", mbti_types)

    # 해당 유형 상위 10개 국가
    sorted_df = df.sort_values(by=selected_type, ascending=False).reset_index(drop=True)
    top10 = sorted_df.head(10)

    # 한국이 포함되어 있지 않으면 마지막에 추가
    if "South Korea" not in top10["Country"].values and "South Korea" in df["Country"].values:
        korea_row = df[df["Country"] == "South Korea"]
        top10 = pd.concat([top10, korea_row], ignore_index=True)

    # 색상 설정
    colors = ["#60a5fa"] * len(top10)  # 기본 파란색 계열
    if "South Korea" in top10["Country"].values:
        idx = top10[top10["Country"] == "South Korea"].index[0]
        colors[idx] = "#00bfa5"  # 청록색

    # 그래프 생성
    fig2 = px.bar(
        top10,
        x="Country",
        y=selected_type,
        color="Country",
        color_discrete_sequence=colors,
        title=f"🌍 {selected_type} 유형이 많은 상위 국가",
    )

    fig2.update_layout(
        showlegend=False,
        xaxis_title="국가",
        yaxis_title="비율",
        plot_bgcolor="white",
        paper_bgcolor="white",
        title_x=0.5,
        font=dict(size=15),
    )
    fig2.update_traces(hovertemplate="<b>%{x}</b><br>비율: %{y:.2%}<extra></extra>")
    st.plotly_chart(fig2, use_container_width=True)
