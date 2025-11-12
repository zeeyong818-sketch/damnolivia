# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import os
from io import BytesIO

st.set_page_config(page_title="Countries MBTI Explorer", layout="wide")

st.title("🌍 Countries MBTI Explorer")
st.markdown(
    "국가별 MBTI 비율을 인터랙티브하게 살펴보세요. "
    "사이드바에서 CSV 파일을 업로드하거나, 프로젝트 루트에 `countriesMBTI_16types.csv` 파일이 있으면 자동으로 불러옵니다."
)

# ---------- 데이터 로드 ----------
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        local_path = "countriesMBTI_16types.csv"
        if os.path.exists(local_path):
            df = pd.read_csv(local_path)
        else:
            st.error(
                "CSV 파일을 찾을 수 없습니다. 사이드바에서 업로드하거나 프로젝트 루트에 "
                "`countriesMBTI_16types.csv` 파일을 올려주세요."
            )
            st.stop()
    # Ensure Country column present
    if "Country" not in df.columns:
        st.error("CSV에 'Country' 열이 필요합니다.")
        st.stop()
    return df

with st.sidebar:
    st.header("데이터 입력")
    uploaded = st.file_uploader("CSV 업로드 (optional)", type=["csv"])
    df = load_data(uploaded)

# ---------- 전처리 ----------
mbti_cols = [c for c in df.columns if c != "Country"]
# Normalize if user uploaded absolute numbers (detect if sums ~1 or ~100)
# But here we assume proportions (0~1). If sums > 1.1, try to normalize per-row.
row_sums = df[mbti_cols].sum(axis=1)
if (row_sums > 1.1).any():
    # likely percentages not normalized -> normalize to proportions
    df[mbti_cols] = df[mbti_cols].div(row_sums, axis=0)

# world average
world_avg = df[mbti_cols].mean().rename("World Average")

# ---------- UI: 국가 선택 ----------
st.sidebar.header("View Options")
countries = ["World Average"] + df["Country"].tolist()
country = st.sidebar.selectbox("국가 선택", countries)

show_table = st.sidebar.checkbox("데이터 테이블 보기", value=True)
show_summary = st.sidebar.checkbox("요약 통계 보기 (mean/std)", value=False)

# ---------- 색 생성 유틸 ----------
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*[int(round(v)) for v in rgb])

def gradient_colors(n, start_hex="#dff8ff", end_hex="#87ceeb"):
    # n: number of colors; interpolate between start and end
    if n == 1:
        return [end_hex]
    s = hex_to_rgb(start_hex)
    e = hex_to_rgb(end_hex)
    colors = []
    for i in range(n):
        t = i / max(n - 1, 1)
        rgb = (s[0] + (e[0]-s[0])*t, s[1] + (e[1]-s[1])*t, s[2] + (e[2]-s[2])*t)
        colors.append(rgb_to_hex(rgb))
    return colors

# ---------- 데이터 선택 ----------
if country == "World Average":
    vals = world_avg
else:
    row = df[df["Country"] == country]
    if row.empty:
        st.error("선택한 국가의 데이터가 없습니다.")
        st.stop()
    vals = row[mbti_cols].iloc[0]

# Sort display order (keep MBTI standard order from columns)
types = mbti_cols
values = [float(vals[t]) for t in types]

# Identify top index
max_idx = int(pd.Series(values).idxmax()) if isinstance(values, list) else pd.Series(values).idxmax()
# But idxmax gave index label; easier:
max_pos = int(pd.Series(values).argmax())

# Build colors: first make gradient for others, then insert green for top
n = len(types)
grad = gradient_colors(n, start_hex="#dff8ff", end_hex="#87ceeb")
# We want top bar to be green; replace that position with green
green_hex = "#2ca02c"  # green
colors = grad.copy()
colors[max_pos] = green_hex

# ---------- Plotly 그래프 ----------
fig = go.Figure(
    data=[
        go.Bar(
            x=types,
            y=values,
            marker_color=colors,
            hovertemplate="%{x}<br>비율: %{y:.4f}<extra></extra>",
        )
    ]
)

fig.update_layout(
    title_text=f"{country} — MBTI 분포",
    xaxis_title="MBTI 타입",
    yaxis_title="비율 (proportion)",
    yaxis=dict(tickformat=".2%"),
    template="plotly_white",
    margin=dict(l=40, r=20, t=70, b=120),
    hovermode="closest",
)

# Rotate x labels for readability
fig.update_xaxes(tickangle=-45)

# ---------- 레이아웃 출력 ----------
col1, col2 = st.columns([3, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("요약")
    st.write(f"선택: **{country}**")
    top_type = types[max_pos]
    top_value = values[max_pos]
    st.markdown(f"- 가장 높은 MBTI: **{top_type}** — {top_value:.2%}")
    if show_summary:
        st.write("**전세계 평균 / 표준편차 (columns)**")
        stats = pd.DataFrame({
            "mean": df[mbti_cols].mean(),
            "std": df[mbti_cols].std()
        }).sort_values("mean", ascending=False)
        st.dataframe(stats.style.format("{:.4f}"))

# 데이터 테이블
if show_table:
    st.subheader("데이터 (선택 국가)")
    display_df = pd.DataFrame({"MBTI": types, "Proportion": values})
    st.dataframe(display_df.style.format({"Proportion": "{:.4f}"}), height=320)

    # CSV 다운로드
    csv = display_df.to_csv(index=False).encode("utf-8")
    st.download_button("선택 데이터 CSV로 다운로드", data=csv, file_name=f"{country.replace(' ', '_')}_mbti.csv", mime="text/csv")

st.markdown("---")
st.caption("앱: Streamlit + Plotly — 1등은 초록, 나머지는 하늘색 그라데이션으로 표시됩니다.")
