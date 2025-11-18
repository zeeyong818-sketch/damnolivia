import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="서울 지하철 역별 승하차 분석", layout="wide")

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    return pd.read_csv("damn.csv", encoding="cp949")

df = load_data()

st.title("🚇 서울 지하철 승하차 분석 (2025년 10월)")

# 날짜 선택
dates = sorted(df["사용일자"].unique())
selected_date = st.selectbox("📅 날짜를 선택하세요", dates)

# 선택한 날짜로 필터
filtered = df[df["사용일자"] == selected_date]

# 노선 선택
lines = sorted(filtered["노선명"].unique())
selected_line = st.selectbox("🚏 호선을 선택하세요", lines)

# 선택한 노선으로 필터
line_df = filtered[filtered["노선명"] == selected_line].copy()

# 총승하차 계산
line_df["총승하차"] = line_df["승차총승객수"] + line_df["하차총승객수"]

# 역별 정렬
line_df = line_df.sort_values("총승하차", ascending=False)

# 1위는 빨간색, 나머지는 파란색 → 파란색 그라데이션 적용
colors = ["red"]  # 1등
blue_shades = px.colors.sequential.Blues[len(line_df) - 1]  # 나머지
colors.extend(blue_shades)

# 그래프 생성
fig = px.bar(
    line_df,
    x="역명",
    y="총승하차",
    title=f"📊 {selected_date} - {selected_line} 승하차 수 Top 역",
    color=line_df.index,  # 더미 색 기준
    color_discrete_sequence=colors
)

# 라벨, 레이아웃 조정
fig.update_layout(
    xaxis_title="역명",
    yaxis_title="총승하차 수",
    showlegend=False
)

# 표시
st.plotly_chart(fig, use_container_width=True)

# 데이터 테이블 보기
st.subheader("📄 데이터 테이블")
st.dataframe(line_df.reset_index(drop=True))
