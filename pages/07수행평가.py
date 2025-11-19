import streamlit as st
import pandas as pd
import io

# 1. 데이터를 불러오는 함수 (Streamlit Cloud 환경에서는 직접 업로드된 파일을 읽습니다.)
@st.cache_data
def load_data():
    # 사용자가 업로드한 'altificial.csv' 파일을 직접 읽습니다.
    # Streamlit 환경에서 'altificial.csv' 파일이 접근 가능하다고 가정합니다.
    try:
        # 데이터가 CSV 형태의 문자열로 처리될 수 있으므로 io.StringIO를 사용합니다.
        # 실제 Streamlit Cloud 배포 시에는 'altificial.csv' 파일을 프로젝트 폴더에 넣어두거나
        # 파일 업로드 위젯을 사용하여 데이터를 받도록 코드를 수정해야 합니다.
        # 여기서는 파일 접근이 가능한 환경임을 가정하고 코드를 작성합니다.
        df = pd.read_csv('altificial.csv', encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv('altificial.csv', encoding='cp949')
        except:
            df = pd.read_csv('altificial.csv', encoding='euc-kr')
    except FileNotFoundError:
        st.error("🚨 'altificial.csv' 파일을 찾을 수 없어요. 파일을 Streamlit 프로젝트 폴더에 넣어주세요!")
        return pd.DataFrame() # 빈 DataFrame 반환

    # 데이터 전처리: '구분', '총점포수' 등 필요한 열의 타입을 정리합니다.
    df['구분'] = df['구분'].str.strip()
    df['주요메뉴'] = df['주요메뉴'].str.strip()
    
    # NaN 값 처리: '체명'의 결측치는 '정보없음'으로 채워줍니다.
    df['체명'] = df['체명'].fillna('정보없음')
    
    return df

# 2. 메인 Streamlit 앱 함수
def app():
    st.set_page_config(layout="wide")
    st.title("🌎 K-브랜드 해외 진출 현황 분석 대시보드")
    st.markdown("---")
    
    # 2. 데이터 불러오기
    df = load_data()
    if df.empty:
        return

    # 3. 사이드바 (사용자가 선택할 수 있는 필터) - MBTI 선택 형식 이용
    with st.sidebar:
        st.header("🔍 분석 필터 설정")
        
        # '구분' (한식/비한식)을 선택하는 위젯
        all_categories = df['구분'].unique().tolist()
        all_categories.insert(0, '전체') # '전체' 옵션 추가
        
        selected_category = st.selectbox(
            "어떤 브랜드 타입을 볼까?",
            options=all_categories, # 16개 MBTI 선택 대신, '구분' 선택
            index=0
        )
        
        # '총점포수' 최소 기준 설정
        min_stores = st.slider(
            "최소 해외 점포수 기준은?",
            min_value=1, 
            max_value=int(df['총점포수'].max()), 
            value=10, # 기본값 10개 이상
            step=1
        )
        
        st.markdown("---")
        st.info("💡 **팁:** 데이터를 필터링해서 자세히 살펴보자!")

    # 4. 필터링된 데이터 준비
    filtered_df = df.copy()
    
    if selected_category != '전체':
        filtered_df = filtered_df[filtered_df['구분'] == selected_category]
        
    filtered_df = filtered_df[filtered_df['총점포수'] >= min_stores]
    
    # 5. 핵심 통계 카드 출력
    col1, col2, col3 = st.columns(3)
    
    with col1:
