import streamlit as st
from streamlit_folium import st_folium
import folium
import math

st.set_page_config(page_title="Seoul Trip Planner", layout="wide")

st.title("🌿 Seoul Top 10 Travel Map — 외국인이 좋아하는 서울 관광지")
st.markdown("초보 여행자를 위한 **가까운 지하철역 + 일정 추천** 지도입니다.")

# 데이터 (관광지 + 지하철 정보)
places = [
    {"name": "Gyeongbokgung Palace (경복궁)", "desc": "조선의 대표적 왕궁.", "lat": 37.579617, "lon": 126.977041,
     "station": "경복궁역", "line": "3호선 (주황색)"},
    {"name": "N Seoul Tower (남산 N타워)", "desc": "서울 전경을 볼 수 있는 랜드마크.", "lat": 37.551169, "lon": 126.988227,
     "station": "명동역 / 서울역", "line": "4호선 (하늘색), 1호선 (남색)"},
    {"name": "Myeongdong (명동)", "desc": "쇼핑과 길거리 음식의 중심.", "lat": 37.563756, "lon": 126.986022,
     "station": "명동역", "line": "4호선 (하늘색)"},
    {"name": "Bukchon Hanok Village (북촌한옥마을)", "desc": "전통 한옥 골목 산책지.", "lat": 37.582604, "lon": 126.983040,
     "station": "안국역", "line": "3호선 (주황색)"},
    {"name": "Insadong (인사동)", "desc": "전통 찻집과 기념품 거리.", "lat": 37.574408, "lon": 126.984984,
     "station": "안국역 / 종로3가역", "line": "3·1·5호선"},
    {"name": "Hongdae (홍대)", "desc": "젊음과 예술의 문화거리.", "lat": 37.556264, "lon": 126.922167,
     "station": "홍대입구역", "line": "2호선 (초록색), 공항철도"},
    {"name": "DDP (동대문디자인플라자)", "desc": "미래적 건축 + 야시장.", "lat": 37.566295, "lon": 127.009410,
     "station": "동대문역사문화공원역", "line": "2·4·5호선"},
    {"name": "Changdeokgung (창덕궁)", "desc": "유네스코 세계유산 궁궐.", "lat": 37.582809, "lon": 126.991003,
     "station": "안국역", "line": "3호선 (주황색)"},
    {"name": "Lotte World Tower (롯데월드타워)", "desc": "초고층 전망대 + 쇼핑.", "lat": 37.513078, "lon": 127.102513,
     "station": "잠실역", "line": "2·8호선"},
    {"name": "Cheonggyecheon (청계천)", "desc": "도심 속 시원한 산책길.", "lat": 37.568422, "lon": 126.977019,
     "station": "종각역 / 을지로입구역", "line": "1·2호선"}
]

# 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12, control_scale=True)
for p in places:
    folium.Marker(
        location=[p["lat"], p["lon"]],
        popup=f"<b>{p['name']}</b><br>{p['desc']}<br><br>"
              f"<b>🚇 지하철:</b> {p['station']}<br>"
              f"<b>노선:</b> {p['line']}",
        tooltip=p["name"],
        icon=folium.Icon(color="green", icon="info-sign")   # ✅ 초록색 마커
    ).add_to(m)

st.markdown("### 🗺 지도")
st_folium(m, width=850, height=520)

st.markdown("---")

# ✅ 일정 생성 기능
st.markdown("### 📅 여행 일정 추천")

days = st.selectbox("여행 일수를 선택하세요:", [1, 2, 3])

def split_list(lst, n):
    k = math.ceil(len(lst) / n)
    return [lst[i:i+k] for i in range(0, len(lst), k)]

schedule = split_list(places, days)

for i, day_plan in enumerate(schedule, 1):
    st.markdown(f"#### Day {i}")
    for p in day_plan:
        st.markdown(f"- **{p['name']}** — {p['station']} ({p['line']})")
    st.write("")

st.caption("🚇 TIP: 지하철 중심으로 이동하면 가장 빠르고 편합니다!")
