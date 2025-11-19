import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="사업체조사 데이터 분석", layout="wide")

st.title("📊 공공데이터포털 사업체조사 대시보드")

# -------------------------
# 데이터 로드
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("you.xlsx")
    return df

df = load_data()

st.success("데이터 로드 완료!")    

# ----------------------------------
# 사이드바 필터
# ----------------------------------
st.sidebar.header("🔍 필터")

selected_region = st.sidebar.selectbox(
    "행정구역 선택",
    options=df["행정구역"].unique()
)

selected_category = st.sidebar.selectbox(
    "산업분류명 선택",
    options=df["산업분류명"].unique()
)

filtered = df[(df["행정구역"] == selected_region) &
              (df["산업분류명"] == selected_category)]

# ----------------------------------
# KPI 카드
# ----------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("총 사업체수", int(filtered["총사업체수"].sum()))
col2.metric("총 종사자수", int(filtered["총종사자수"].sum()))
col3.metric("남자 종사자수", int(filtered["남자종사자수"].sum()))
col4.metric("여자 종사자수", int(filtered["여자종사자수"].sum()))

st.divider()

# ----------------------------------
# 산업분류명별 사업체수 비교 (막대그래프)
# ----------------------------------
st.subheader("📌 산업분류명별 총사업체수 비교")

grouped = df.groupby("산업분류명")["총사업체수"].sum().reset_index()

fig1 = px.bar(
    grouped,
    x="산업분류명",
    y="총사업체수",
    title="전체 산업분류 대비 사업체수",
)

st.plotly_chart(fig1, use_container_width=True)

st.divider()

# ----------------------------------
# 행정구역별 종사자수 비교
# ----------------------------------
st.subheader("📌 행정구역별 총종사자수")

grouped2 = df.groupby("행정구역")["총종사자수"].sum().reset_index()

fig2 = px.bar(
    grouped2,
    x="행정구역",
    y="총종사자수",
    title="행정구역별 총종사자수",
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------
# 대표자 나이대 분석
# ----------------------------------
st.subheader("📌 대표자 연령대별 사업체수")

age_cols = [
    "대표자사업체수20세미만",
    "대표자사업체수20_29세",
    "대표자사업체수30_39세",
    "대표자사업체수40_49세",
    "대표자사업체수50_59세",
    "대표자사업체수60세이상",
]

age_df = df[age_cols].sum().reset_index()
age_df.columns = ["연령대", "사업체수"]

fig3 = px.bar(age_df, x="연령대", y="사업체수", title="대표자 연령대별 사업체수")

st.plotly_chart(fig3, use_container_width=True)
