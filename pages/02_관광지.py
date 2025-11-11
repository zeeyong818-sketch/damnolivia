st.markdown("### 📅 여행 일정 추천 (시간대별)")

days = st.selectbox("여행 일수를 선택하세요:", [1, 2, 3])

# 지역별 묶음 (이동 최소화)
clusters = [
    ["Gyeongbokgung Palace (경복궁)", "Bukchon Hanok Village (북촌한옥마을)", "Changdeokgung (창덕궁)", "Insadong (인사동)", "Cheonggyecheon (청계천)"],
    ["Myeongdong (명동)", "N Seoul Tower (남산 N타워)"],
    ["DDP (동대문디자인플라자)"],
    ["Hongdae (홍대)"],
    ["Lotte World Tower (롯데월드타워)"]
]

# 관광지 이름 → 데이터 매핑
place_map = {p["name"]: p for p in places}

# 여행 일수만큼 cluster 채택
selected_clusters = clusters[:days]

def format_plan(title, place, meal=None):
    if meal:
        return f"**{title}** 🍽 — *{meal}*\n"
    return f"**{title}** — {place['name']} (🚇 {place['station']} / {place['line']})\n"

for day, cluster in enumerate(selected_clusters, 1):
    spot_data = [place_map[name] for name in cluster]

    st.markdown(f"#### 🌿 Day {day}")

    # 시간대별 배치
    schedule_plan = []
    if len(spot_data) >= 1:
        schedule_plan.append(format_plan("오전", spot_data[0]))
    if len(spot_data) >= 2:
        schedule_plan.append(format_plan("오후", spot_data[1]))
    if len(spot_data) >= 3:
        schedule_plan.append(format_plan("야간", spot_data[2]))

    # 지역별 일반적인 식사 추천 (심플 버전)
    lunch = "현지 맛집 추천 (점심)"
    dinner = "가성비 + 분위기 좋은 저녁 식사 추천"

    schedule_plan.insert(1, format_plan("점심", None, meal=lunch))
    schedule_plan.insert(-1, format_plan("저녁", None, meal=dinner))

    # 출력
    for line in schedule_plan:
        st.markdown(line)
