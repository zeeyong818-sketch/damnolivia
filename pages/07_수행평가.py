import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 설정 및 데이터 로드 ---

# 페이지 설정
st.set_page_config(
    page_title="지역별 베이커리·카페 현황 분석",
    page_icon="🍩",
    layout="wide"
)

# 캐시를 사용하여 데이터 로딩 속도를 높입니다.
@st.cache_data
def load_data():
    # CSV 파일을 로드합니다. (한글 인코딩 문제 대비)
    try:
        df = pd.read_csv("../damngyugyugyugyugyugyugyugyuguygug.csv", encoding='cp949')
    except UnicodeDecodeError:
        df = pd.read_csv("../damngyugyugyugyugyugyugyugyuguygug.csv", encoding='euc-kr')
    except FileNotFoundError:
        st.error("CSV 파일을 찾을 수 없습니다. 파일 이름과 경로를 확인해주세요.")
        return pd.DataFrame()

    # '산업분류명'에서 '베이커리', '카페', '음료' 등이 포함된 행만 필터링합니다.
    # 해당 데이터 스니펫의 '산업분류명'을 바탕으로 필터링 조건을 설정했습니다.
    keywords = ['제과점', '커피전문점', '음료']
    df_filtered = df[df['산업분류명'].astype(str).str.contains('|'.join(keywords), na=False)]

    # '행정구역'이 '전국'인 행은 전체 합계이므로 제외합니다.
    df_filtered = df_filtered[df_filtered['행정구역'] != '전국'].copy()

    # 필요한 컬럼만 선택하고 숫자로 변환 (오류 무시)
    cols_to_convert = ['총사업체수', '총종사자수', '남자종사자수', '여자종사자수']
    for col in cols_to_convert:
        # 'X'와 같은 문자열 데이터를 NaN으로 만든 후 0으로 채우고 정수로 변환합니다.
        df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce').fillna(0).astype(int)

    return df_filtered

df = load_data()

# 데이터가 비어있으면 오류 메시지 출력 후 종료
if df.empty:
    st.stop()


# --- 대시보드 제목 및 필터 ---

st.title("🍩 지역별 베이커리·카페 사업체 현황 분석 대시보드")
st.markdown("깔끔하고 인터랙티브한 시각화를 통해 지역별 사업체 수 및 종사자 현황을 확인합니다.")

# 사이드바 설정
st.sidebar.header("📊 분석 항목 선택")

# 측정 항목 선택 (Key Metrics)
metrics_options = {
    "총사업체수": "총사업체수",
    "총종사자수": "총종사자수",
    "남자종사자수": "남자종사자수",
    "여자종사자수": "여자종사자수"
}
selected_metric_name = st.sidebar.selectbox(
    "주요 측정 항목을 선택하세요:",
    list(metrics_options.keys())
)
selected_metric_col = metrics_options[selected_metric_name]

# 지역 필터링
all_regions = ['전체'] + sorted(df['행정구역'].unique().tolist())
selected_region = st.sidebar.selectbox(
    "분석할 지역을 선택하세요:",
    all_regions
)


# --- 시각화 함수 ---

# 1. 지역별 현황 막대 그래프
def plot_regional_bar(data, metric_col, metric_name):
    # '행정구역'별로 선택된 측정 항목의 합계를 구합니다.
    df_plot = data.groupby('행정구역')[metric_col].sum().reset_index()

    fig = px.bar(
        df_plot,
        x='행정구역',
        y=metric_col,
        title=f"**지역별 {metric_name} 비교**",
        color=metric_col,  # 값에 따라 색상 변화
        color_continuous_scale=px.colors.sequential.Teal, # 색상 팔레트
        labels={'행정구역': '행정구역', metric_col: metric_name},
        template="plotly_white"
    )

    fig.update_layout(xaxis={'categoryorder':'total descending'}) # 내림차순 정렬
    st.plotly_chart(fig, use_container_width=True)


# 2. 남녀 종사자 비율 파이 차트
def plot_gender_ratio(data, region_name):
    total_male = data['남자종사자수'].sum()
    total_female = data['여자종사자수'].sum()

    gender_data = pd.DataFrame({
        '성별': ['남자', '여자'],
        '종사자수': [total_male, total_female]
    })

    title = f"**{region_name}** 베이커리·카페 종사자 성별 비율"
    if total_male + total_female == 0:
        st.warning(f"선택된 지역({region_name})에 해당하는 종사자 데이터가 없습니다.")
        return

    fig = px.pie(
        gender_data,
        values='종사자수',
        names='성별',
        title=title,
        color_discrete_sequence=['#4CAF50', '#2196F3'], # 초록색, 파란색 (크리에이티브 & 깔끔한 색상)
        template="plotly_white"
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)


# --- 대시보드 레이아웃 ---

# 데이터 필터링 적용
if selected_region != '전체':
    df_plot = df[df['행정구역'] == selected_region]
    region_display_name = selected_region
else:
    df_plot = df
    region_display_name = "전국 (선택된 산업군)"


# 첫 번째 행: 요약 정보 (KPLs)
col1, col2, col3, col4 = st.columns(4)

total_businesses = df_plot['총사업체수'].sum()
total_employees = df_plot['총종사자수'].sum()
avg_employees = total_employees / total_businesses if total_businesses else 0
female_ratio = (df_plot['여자종사자수'].sum() / total_employees) * 100 if total_employees else 0

with col1:
    st.metric(label="총 사업체 수", value=f"{total_businesses:,} 개")
with col2:
    st.metric(label="총 종사자 수", value=f"{total_employees:,} 명")
with col3:
    st.metric(label="사업체당 평균 종사자", value=f"{avg_employees:.1f} 명")
with col4:
    st.metric(label="여자 종사자 비율", value=f"{female_ratio:.1f} %")

st.markdown("---")

# 두 번째 행: 그래프 (지역별 막대 그래프 & 성별 비율 파이 차트)
col_bar, col_pie = st.columns([2, 1])

with col_bar:
    plot_regional_bar(df, selected_metric_col, selected_metric_name)

with col_pie:
    plot_gender_ratio(df_plot, region_display_name)

st.markdown("---")

# 세 번째 행: 원본 데이터 확인 (선택 사항)
if st.checkbox("원본 데이터 테이블 보기"):
    st.subheader(f"{region_display_name} 데이터 테이블")
    st.dataframe(df_plot)
