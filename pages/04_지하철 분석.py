# pages/01_역별_승하차_분석.py
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.colors import n_colors

st.set_page_config(page_title="서울 지하철 역별 승하차 분석", layout="wide")

st.title("🚇 서울 지하철 승하차 분석 (2025년 10월)")

@st.cache_data
def load_data(path="damn.csv"):
    # 인코딩 여러가지 시도 (utf-8 실패하면 cp949로)
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except Exception:
        df = pd.read_csv(path, encoding="cp949")
    return df

# --- 로드 ---
try:
    df = load_data("damn.csv")
except FileNotFoundError:
    st.error("파일을 찾을 수 없습니다: 루트 폴더에 `damn.csv`가 있는지 확인하세요.")
    st.stop()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 컬럼명 정리 (혹시 공백/유니코드 문제가 있으면 안전하게)
df.columns = df.columns.str.strip()

# 사용일자 문자열로 바꾸기
df["사용일자"] = df["사용일자"].astype(str)

# 2025년 10월(202510**) 데이터만 선택 가능한 옵션으로 제공
oct_2025 = sorted([d for d in df["사용일자"].unique() if d.startswith("202510")])
if not oct_2025:
    st.error("데이터에 2025년 10월(예: 20251001) 기록이 없습니다. CSV를 확인해 주세요.")
    st.stop()

selected_date = st.selectbox("📅 2025년 10월 중 하루를 선택하세요", oct_2025)

# 선택한 날짜로 필터
filtered = df[df["사용일자"] == selected_date].copy()

# 노선 선택
lines = sorted(filtered["노선명"].unique())
if not lines:
    st.error("선택한 날짜에 해당하는 노선 데이터가 없습니다.")
    st.stop()

selected_line = st.selectbox("🚏 호선을 선택하세요", lines)

# 선택한 노선으로 필터
line_df = filtered[filtered["노선명"] == selected_line].copy()

# 숫자형으로 안전하게 변환
for col in ["승차총승객수", "하차총승객수"]:
    line_df[col] = pd.to_numeric(line_df[col], errors="coerce").fillna(0).astype(int)

# 총승하차 계산 및 정렬
line_df["총승하차"] = line_df["승차총승객수"] + line_df["하차총승객수"]
line_df = line_df.sort_values("총승하차", ascending=False).reset_index(drop=True)

if line_df.empty:
    st.warning("해당 노선/날짜에 데이터가 없습니다.")
    st.stop()

# 상위 10개만 (요구대로 10개)
top_n = 10
top_df = line_df.head(top_n).copy()

# 색상 생성: 1등은 빨간색, 나머지는 파란색-그라데이션
n_rest = max(len(top_df) - 1, 0)
if n_rest > 0:
    # 연한 파랑 -> 진한 파랑 그라데이션 (n_colors 사용)
    blues = n_colors('rgb(198,219,239)', 'rgb(8,48,107)', n_rest, colortype='rgb')
else:
    blues = []

colors = ["red"] + blues  # 길이는 top_df 행수와 같아야 함

# plotly: 각 막대에 색 할당하려면 color에 '역명'을 사용하고 color_discrete_sequence 전달
fig = px.bar(
    top_df,
    x="역명",
    y="총승하차",
    title=f"📊 {selected_date} · {selected_line} - 총승하차 Top {len(top_df)}",
    color="역명",
    color_discrete_sequence=colors,
    text="총승하차",
)

fig.update_traces(texttemplate="%{text:,}", textposition="outside")
fig.update_layout(
    xaxis_title="역명",
    yaxis_title="총승하차 수",
    showlegend=False,
    uniformtext_minsize=8,
    uniformtext_mode="hide",
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📄 데이터 (상위 항목)")
st.dataframe(top_df.reset_index(drop=True))
