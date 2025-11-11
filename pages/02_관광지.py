import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Seoul Top10 Map (For Foreigners)", layout="wide")

st.title("🌏 Seoul Top10 — 외국인이 좋아하는 서울 주요 관광지 (Folium)")
st.markdown("""
서울을 처음 방문하는 외국인들이 특히 선호하는 **Top 10 관광지**를 지도에 표시했습니다.
사이드바에서 장소를 선택하면 지도 중심이 해당 장소로 이동하고, 마커를 클릭하면 간단한 설명이 나옵니다.
""")

# 장소 목록 (이름, 설명, 위도, 경도)
places = [
    {"name": "Gyeongbokgung Palace (경복궁)", "desc": "조선의 대표적 왕궁 — 전통 건축과 수문장 교대식으로 유명합니다.", "lat": 37.579617, "lon": 126.977041},
    {"name": "N Seoul Tower / Namsan (N서울타워 / 남산)", "desc": "서울의 대표 랜드마크, 야경과 전경이 아름답습니다.", "lat": 37.551169, "lon": 126.988227},
    {"name": "Myeongdong (명동)", "desc": "쇼핑과 길거리음식이 활발한 대표 상업지구.", "lat": 37.563756, "lon": 126.986022},
    {"name": "Bukchon Hanok Village (북촌한옥마을)", "desc": "한옥 골목을 걸으며 전통가옥을 볼 수 있는 지역.", "lat": 37.582604, "lon": 126.983040},
    {"name": "Insadong (인사동)", "desc": "한국 전통문화, 기념품, 찻집이 모여 있는 문화거리.", "lat": 37.574408, "lon": 126.984984},
    {"name": "Hongdae (홍대)", "desc": "젊음의 거리·라이브 음악·카페 문화 중심지.", "lat": 37.556264, "lon": 126.922167},
    {"name": "Dongdaemun Design Plaza (DDP)", "desc": "독특한 건축물과 야시장, 패션·디자인 거리.", "lat": 37.566295, "lon": 127.009410},
    {"name": "Changdeokgung Palace & Secret Garden (창덕궁)", "desc": "유네스코 세계유산 — 비원(후원) 관광이 유명.", "lat": 37.582809, "lon": 126.991003},
    {"name": "Lotte World Tower / Seoul Sky (롯데월드타워)", "desc": "123층 초고층 전망대와 쇼핑 엔터테인먼트 복합공간.", "lat": 37.513078, "lon": 127.102513},
    {"name": "Cheonggyecheon Stream (청계천)", "desc": "도심 속 하천 산책로 — 낮과 밤 모두 인기.", "lat": 37.568422, "lon": 126.977019}
]

# 지도 생성
def make_map(center=[37.5665, 126.9780], zoom=12):
    m = folium.Map(location=center, zoom_start=zoom, control_scale=True)
    for p in places:
        folium.Marker(
            location=[p["lat"], p["lon"]],
            popup=f"<b>{p['name']}</b><br>{p['desc']}",
            tooltip=p["name"],
            icon=folium.Icon(color="red", icon="info-sign")  # ✅ 빨간색 마커
        ).add_to(m)
    return m

# 사이드바
st.sidebar.header("📍 장소 바로가기 (Top 10)")
place_names = ["전체보기"] + [p["name"] for p in places]
choice = st.sidebar.selectbox("장소를 선택하세요:", place_names)

# 선택 시 중심 이동
if choice == "전체보기":
    m = make_map()
else:
    selected = next(p for p in places if p["name"] == choice)
    m = make_map(center=[selected["lat"], selected["lon"]], zoom=15)

# 지도 표시 — ✅ 크기 줄임 (약 70%)
st.markdown("### 🗺️ 서울 관광지도")
st_folium(m_
