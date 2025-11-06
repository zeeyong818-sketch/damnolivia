# app.py
import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천 🎯", page_icon="🧭", layout="centered")

st.title("✨ MBTI로 찾는 진로 추천 (청소년용) ✨")
st.caption("MBTI를 하나 골라봐요 — 그 유형에 잘 맞는 진로, 관련 도서·영화, 적합 학과와 성격을 알려줄게요! 😊")

MBTI_OPTIONS = [
    "ISTJ","ISFJ","INFJ","INTJ",
    "ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP",
    "ESTJ","ESFJ","ENFJ","ENTJ"
]

data = {
    "ISTJ": {
        "careers": ["공무원 / 행정직", "회계사 / 세무사"],
        "books": ["『성공하는 사람들의 7가지 습관』 - 스티븐 코비", "『회계의 신 기본기』 (입문서)"],
        "movies": ["《The Pursuit of Happyness》(행복을 찾아서)", "《A Beautiful Mind》(뷰티풀 마인드)"],
        "majors": "행정학, 경영학(회계), 세무·경제 관련 학과",
        "personality": "규칙적이고 책임감 강함. 디테일을 잘 챙기고 안정적인 환경을 좋아해요. ✅"
    },
    "ISFJ": {
        "careers": ["간호사 / 보건의료", "초등교사 / 아동·복지 관련"],
        "books": ["『보건의료와 인간』 (실무 입문서)", "『가르치기의 기쁨』 (교육 입문 관련)"],
        "movies": ["《The Help》(헬프)", "《Pay It Forward》(남겨진 선물)"],
        "majors": "간호학, 보건학, 아동·복지학, 교육학",
        "personality": "따뜻하고 헌신적. 사람 챙기기를 좋아하며 안정적이고 실용적인 일을 잘해요. 🌱"
    },
    "INFJ": {
        "careers": ["상담심리사 / 임상심리사", "작가 / 창작자(문학)"],
        "books": ["『Man’s Search for Meaning』 - Viktor Frankl", "『그릿(Grit)』 - Angela Duckworth"],
        "movies": ["《Inside Out》(인사이드 아웃)", "《Good Will Hunting》(굿 윌 헌팅)"],
        "majors": "심리학, 문예창작, 상담학",
        "personality": "이해심 깊고 통찰력 있음. 사람의 마음과 의미를 찾는 일을 잘 해요. 🌙"
    },
    "INTJ": {
        "careers": ["전략기획 / 컨설턴트", "연구원(과학·기술 분야)"],
        "books": ["『Thinking, Fast and Slow』 - Daniel Kahneman", "『The Lean Startup』 - Eric Ries"],
        "movies": ["《The Imitation Game》(이미테이션 게임)", "《Interstellar》(인터스텔라)"],
        "majors": "경영학(전략), 산업공학, 컴퓨터공학, 순수·응용과학",
        "personality": "전략적이고 계획적. 복잡한 문제를 분석하고 장기적 목표를 세우는 걸 좋아해요. 🧠"
    },
    "ISTP": {
        "careers": ["기계·설계 엔지니어", "응급구조사 / 테크니션"],
        "books": ["『Make: Electronics』 (전자 입문서)", "『工学 입문서(실무형)』 (기술 실무)"],
        "movies": ["《Moneyball》(머니볼)", "《Ford v Ferrari》(포드 V 페라리)"],
        "majors": "기계공학, 전기·전자공학, 응급구조학",
        "personality": "손재주 좋고 현실적. 문제를 직접 만져보고 해결하는 실무형이에요. 🔧"
    },
    "ISFP": {
        "careers": ["시각디자이너 / 일러스트레이터", "환경·동물 관련 활동가"],
        "books": ["『Steal Like an Artist』 - Austin Kleon", "『아트의 즐거움』 (입문서)"],
        "movies": ["《Amélie》(아멜리에)", "《Fantastic Mr. Fox》(판타스틱 Mr. 폭스)"],
        "majors": "시각디자인, 미술·공예, 환경학",
        "personality": "감성적이고 예술적. 자유롭게 창작하고 자연과 조화되는 일을 좋아해요. 🎨"
    },
    "INFP": {
        "careers": ["작가 / 시나리오 작가", "NGO·인권 활동가"],
        "books": ["『The Alchemist』 - Paulo Coelho", "『On Writing』 - Stephen King"],
        "movies": ["《Into the Wild》(인투 더 와일드)", "《Eternal Sunshine of the Spotless Mind》(이터널 선샤인)"],
        "majors": "문예창작, 사회학, 국제관계학",
        "personality": "이상과 가치 중심. 의미 있는 이야기나 가치를 전하는 일을 좋아해요. ✨"
    },
    "INTP": {
        "careers": ["데이터 사이언티스트 / 연구개발(R&D)", "소프트웨어 개발자"],
        "books": ["『Gödel, Escher, Bach』 - Douglas Hofstadter", "『Python Crash Course』 (입문서)"],
        "movies": ["《The Social Network》(소셜 네트워크)", "《Primer》(프라이머)"],
        "majors": "컴퓨터공학, 통계학, 수학, 물리학",
        "personality": "논리적이고 호기심 많음. 새로운 아이디어와 시스템 설계에 강해요. 💡"
    },
    "ESTP": {
        "careers": ["영업·마케팅 (현장)", "이벤트·무대 연출가"],
        "books": ["『How to Win Friends & Influence People』 - Dale Carnegie", "『Influence』 - Robert Cialdini"],
        "movies": ["《Catch Me If You Can》(캐치 미 이프 유 캔)", "《The Wolf of Wall Street》(울프 오브 월스트리트)"],
        "majors": "경영학(마케팅), 공연·미디어학",
        "personality": "활발하고 빠른 판단력. 사람을 이끄는 현장형 활동에 강해요. ⚡"
    },
    "ESFP": {
        "careers": ["무대·방송 연예(퍼포먼스)", "패션·뷰티 관련 직종"],
        "books": ["『The Artist's Way』 - Julia Cameron", "『패션 입문서』 (실무형)"],
        "movies": ["《La La Land》(라라랜드)", "《Mamma Mia!》(맘마미아!)"],
        "majors": "공연예술, 미디어학, 패션디자인",
        "personality": "사교적이고 표현력이 풍부. 사람들 앞에서 빛나는 일을 좋아해요. ✨🎤"
    },
    "ENFP": {
        "careers": ["창업가 / 스타트업 마케터", "콘텐츠 크리에이터"],
        "books": ["『The War of Art』 - Steven Pressfield", "『Start with Why』 - Simon Sinek"],
        "movies": ["《The Secret Life of Walter Mitty》(월터의 상상은 현실이 된다)", "《Yes Man》(예스맨)"],
        "majors": "경영학(창업), 미디어·커뮤니케이션, 디자인",
        "personality": "아이디어 넘치고 열정적. 새롭고 사람들 마음을 움직이는 일을 즐겨요. 🔥"
    },
    "ENTP": {
        "careers": ["제품기획(프로덕트 매니저)", "창업·비즈니스 전략가"],
        "books": ["『Zero to One』 - Peter Thiel", "『The Lean Startup』 - Eric Ries"],
        "movies": ["《The Social Network》(소셜 네트워크)", "《The Big Short》(빅 쇼트)"],
        "majors": "경영학, 산업공학, 컴퓨터공학",
        "personality": "발상 전환이 빠르고 논쟁을 즐김. 새 기회를 찾아 실험하는 걸 좋아해요. 🚀"
    },
    "ESTJ": {
        "careers": ["프로젝트 매니저", "법조계(검사·변호사)"],
        "books": ["『Getting Things Done』 - David Allen", "『법학 입문(사전)』 (기초서)"],
        "movies": ["《A Few Good Men》(군인들은 진실을 말한다)", "《Erin Brockovich》(에린 브로코비치)"],
        "majors": "경영학, 법학, 공학(프로젝트 계열)",
        "personality": "조직적이고 결단력 있음. 규칙과 효율을 중시하는 리더형이에요. 🏁"
    },
    "ESFJ": {
        "careers": ["HR(인사)·조직관리", "병원·학교 행정(지원)"],
        "books": ["『Emotional Intelligence』 - Daniel Goleman", "『사람을 읽는 기술』 (대인관계 입문)"],
        "movies": ["《The Blind Side》(블라인드 사이드)", "《The Intouchables》(언터처블: 1%의 우정)"],
        "majors": "인적자원관리, 교육학, 사회복지학",
        "personality": "사교적이고 책임감. 다른 사람을 도와 조직을 원활하게 만드는 걸 좋아해요. 🤝"
    },
    "ENFJ": {
        "careers": ["교육자·리더십 코치", "공공외교·국제기구 활동가"],
        "books": ["『Leaders Eat Last』 - Simon Sinek", "『Drive』 - Daniel H. Pink"],
        "movies": ["《Remember the Titans》(타이탄)", "《Freedom Writers》(프리덤 라이터스)"],
        "majors": "교육학, 국제관계학, 리더십·커뮤니케이션",
        "personality": "사람을 이끄는 능력 탁월. 비전 제시와 사람 성장에 강해요. 🌟"
    },
    "ENTJ": {
        "careers": ["경영자·CEO", "전략컨설팅·투자(VC/PE)"],
        "books": ["『Good to Great』 - Jim Collins", "『The Hard Thing About Hard Things』 - Ben Horowitz"],
        "movies": ["《The Social Network》(소셜 네트워크)", "《Wall Street》(월스트리트)"],
        "majors": "경영학(회계·전략), 경제학, 산업공학",
        "personality": "목표지향적이고 리더십 강함. 큰 그림을 그리고 조직을 이끌어요. 👑"
    }
}

st.write("👉 MBTI를 선택해줘")
choice = st.selectbox("나의 MBTI", MBTI_OPTIONS)

if choice:
    info = data.get(choice, None)
    if info:
        st.markdown("---")
        st.header(f"{choice}님, 이런 진로 어때요? 💡")
        c1, c2 = info["careers"]
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"1️⃣ {c1}")
            st.write("• 어떤 학과가 잘 맞을까?")
            st.info(info["majors"])
            st.write("• 어떤 성격이 잘 맞을까?")
            st.write(info["personality"])
        with col2:
            st.subheader(f"2️⃣ {c2}")
            st.write("• 어떤 학과가 잘 맞을까?")
            st.info(info["majors"])
            st.write("• 어떤 성격이 잘 맞을까?")
            st.write(info["personality"])

        st.markdown("### 📚 관련 추천 도서 (입문/영감용)")
        for b in info["books"]:
            st.write(f"- {b}")

        st.markdown("### 🎬 추천 영화 (분위기로 느낌을 얻어봐!)")
        for m in info["movies"]:
            st.write(f"- {m}")

        st.markdown("---")
        st.write("📝 짧팁 — 진로 고르는 팁")
        st.write("1. 좋아하는 활동을 3개 적어보고, 위 진로와 연결해봐요. ✍️")
        st.write("2. 관심 학과의 수업을 유튜브나 학교 설명회로 먼저 체험해봐요. 🎧")
        st.write("3. 작은 프로젝트나 동아리 활동으로 '해보는 것'이 가장 큰 답을 줘요. 🚀")
        st.success("더 자세히 원하면, 선택한 진로 중 하나를 골라줘. 그 진로에 대해 학교 추천, 세부 직무, 준비 방법까지 알려줄게요! 😉")
    else:
        st.error("아직 준비된 정보가 없어요. 다른 유형을 골라볼래요? 😊")
