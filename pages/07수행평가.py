# streamlit_app.py
import os
import io
from datetime import datetime
from typing import Optional

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from dotenv import load_dotenv

# load .env
load_dotenv()

# ---------------------------
# 설정 및 DB 연결
# ---------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///recipes.db")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# ---------------------------
# DB 모델
# ---------------------------
class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    main_ingredients = Column(Text, nullable=False)
    sub_ingredients = Column(Text, nullable=True)
    method = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    source_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

Base.metadata.create_all(bind=engine)


# ---------------------------
# DB 유틸리티
# ---------------------------
def get_session():
    return SessionLocal()

def add_recipe(session, **kwargs):
    r = Recipe(**kwargs)
    session.add(r)
    session.commit()
    session.refresh(r)
    return r

def update_recipe(session, recipe_id, **kwargs):
    r = session.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not r:
        return None
    for k, v in kwargs.items():
        setattr(r, k, v)
    r.updated_at = datetime.utcnow()
    session.commit()
    session.refresh(r)
    return r

def delete_recipe(session, recipe_id):
    r = session.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not r:
        return False
    session.delete(r)
    session.commit()
    return True

def query_recipes(session, search=None, main_filter=None):
    q = session.query(Recipe)
    if search:
        like = f"%{search}%"
        q = q.filter((Recipe.name.ilike(like)) | (Recipe.main_ingredients.ilike(like)) | (Recipe.method.ilike(like)))
    if main_filter:
        like = f"%{main_filter}%"
        q = q.filter(Recipe.main_ingredients.ilike(like))
    return q.order_by(Recipe.id.desc()).all()

def df_from_recipes(recipes):
    rows = []
    for r in recipes:
        rows.append({
            "id": r.id,
            "요리명": r.name,
            "주재료": r.main_ingredients,
            "부재료": r.sub_ingredients,
            "조리법": r.method,
            "상세설명": r.description,
            "데이터기준일자": r.source_date.isoformat() if r.source_date else None,
            "created_at": r.created_at,
            "updated_at": r.updated_at
        })
    return pd.DataFrame(rows)

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="보성군 차·디저트 DB", layout="wide", initial_sidebar_state="expanded")

# 페이지 헤더 (컬러풀)
st.markdown(
    """
    <div style="display:flex;align-items:center;gap:16px">
      <div style="width:56px;height:56px;border-radius:12px;background:linear-gradient(135deg,#7BD389,#2DBA6A);display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;font-size:22px">茶</div>
      <div>
        <h1 style="margin:0;padding:0;">보성군 차·디저트 레시피 DB</h1>
        <p style="margin:0;color:gray;">컬러풀 · 인터랙티브 · CRUD 지원</p>
      </div>
    </div>
    """, unsafe_allow_html=True
)

# 사이드바: 관리자 로그인, 업로드, 필터
with st.sidebar:
    st.subheader("관리자 접근")
    pw = st.text_input("관리자 비밀번호", type="password")
    is_admin = (pw == ADMIN_PASSWORD)
    if is_admin:
        st.success("관리자 인증됨")
    else:
        st.info("읽기 전용 모드 (데이터 보기 가능). 수정은 관리자만 가능.")

    st.markdown("---")
    st.subheader("파일 업로드")
    uploaded = st.file_uploader("CSV 업로드 (UTF-8 또는 CP949)", type=["csv"])
    if uploaded is not None:
        try:
            df_uploaded = pd.read_csv(uploaded)
        except Exception:
            uploaded.seek(0)
            df_uploaded = pd.read_csv(uploaded, encoding="cp949")
        st.write("업로드 미리보기:")
        st.dataframe(df_uploaded.head(5))

        if st.button("CSV -> DB로 저장 (덮어쓰기 아님)"):
            session = get_session()
            count = 0
            for _, row in df_uploaded.iterrows():
                # 가능한 열 이름 매핑
                name = row.get("요리명") or row.get("name") or row.get("title")
                main = row.get("주재료") or row.get("주재료") or row.get("main_ingredients") or ""
                sub = row.get("부재료") or row.get("부재료") or row.get("sub_ingredients") or ""
                method = row.get("조리법") or row.get("method") or ""
                desc = row.get("상세설명") or row.get("description") or ""
                date_raw = row.get("데이터기준일자") or row.get("source_date") or ""
                try:
                    date_parsed = None
                    if pd.notna(date_raw) and str(date_raw).strip() != "":
                        date_parsed = pd.to_datetime(date_raw).date()
                except Exception:
                    date_parsed = None
                if pd.isna(name):
                    continue
                add_recipe(session,
                           name=str(name).strip(),
                           main_ingredients=str(main).strip(),
                           sub_ingredients=str(sub).strip() if pd.notna(sub) else None,
                           method=str(method).strip(),
                           description=str(desc).strip() if pd.notna(desc) else None,
                           source_date=date_parsed)
                count += 1
            st.success(f"{count}건 DB에 저장 완료")
            session.close()

    st.markdown("---")
    st.subheader("검색 / 필터")
    search = st.text_input("키워드 검색 (요리명, 주재료, 조리법)")
    main_filter = st.text_input("주재료로 필터 (예: 녹차)")

# 메인: 데이터 조회
session = get_session()
recipes = query_recipes(session, search=search, main_filter=main_filter)
df = df_from_recipes(recipes)

# 색상 레이블 컬럼 추가 (프론트 전용)
def label_color(row):
    # 간단 규칙: '녹차' 포함 -> 녹색 계열, '케이크'나 '쿠키' -> 분홍/오렌지, '라떼'나 '티' -> 파란톤
    name = (row.get("요리명") or "").lower()
    main = (row.get("주재료") or "").lower()
    if "녹차" in name or "녹차" in main or "말차" in name or "말차" in main:
        return "녹차"
    if "케이크" in name or "쿠키" in name or "마카롱" in name or "타르트" in name:
        return "디저트"
    if "라떼" in name or "티" in name or "차" in name:
        return "음료"
    return "기타"

if not df.empty:
    df["label"] = df.apply(label_color, axis=1)
else:
    df["label"] = []

# 요약 카드
col1, col2, col3 = st.columns([2,2,6])
with col1:
    st.metric("총 레시피 수", len(df))
with col2:
    st.metric("녹차 레시피 (예상)", (df['label'] == '녹차').sum())
with col3:
    st.write("")

# AgGrid 인터랙티브 표 표시
st.markdown("### 레시피 목록 (클릭 → 상세 / 수정 / 삭제)")
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection(selection_mode="single", use_checkbox=True)
gb.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=10)
# 컬러 스타일 규칙
cellstyle_jscode = """
function(params) {
    if (params.data.label == '녹차') {return {'backgroundColor':'#e8f8f1'}}
    if (params.data.label == '디저트') {return {'backgroundColor':'#fff2f0'}}
    if (params.data.label == '음료') {return {'backgroundColor':'#f0f8ff'}}
    return null;
};
"""
gb.configure_default_column(cellStyle=cellstyle_jscode)
gb.configure_grid_options(domLayout='normal')
grid_options = gb.build()

grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    enable_enterprise_modules=False,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    fit_columns_on_grid_load=True,
    height=450
)

selected = grid_response.get('selected_rows', [])
if selected:
    selected = selected[0]
    st.markdown("---")
    st.subheader("선택된 레시피 상세")
    st.write(f"**요리명:** {selected.get('요리명')}")
    st.write(f"**주재료:** {selected.get('주재료')}")
    st.write(f"**부재료:** {selected.get('부재료')}")
    st.write("**조리법:**")
    st.write(selected.get("조리법"))
    st.write("**상세설명:**")
    st.write(selected.get("상세설명"))

    if is_admin:
        st.markdown("**관리자: 수정 / 삭제**")
        with st.form("edit_form"):
            new_name = st.text_input("요리명", value=selected.get("요리명"))
            new_main = st.text_input("주재료", value=selected.get("주재료"))
            new_sub = st.text_input("부재료", value=selected.get("부재료") or "")
            new_method = st.text_area("조리법", value=selected.get("조리법"))
            new_desc = st.text_area("상세설명", value=selected.get("상세설명") or "")
            submitted = st.form_submit_button("저장")
            if submitted:
                try:
                    update_recipe(session, int(selected.get("id")), name=new_name, main_ingredients=new_main,
                                  sub_ingredients=new_sub, method=new_method, description=new_desc)
                    st.success("수정 완료")
                except Exception as e:
                    st.error(f"수정 실패: {e}")

        if st.button("레시피 삭제"):
            if delete_recipe(session, int(selected.get("id"))):
                st.success("삭제되었습니다. 새로고침 해주세요.")
            else:
                st.error("삭제 실패")
    else:
        st.info("수정/삭제는 관리자만 가능합니다.")

# 레코드 추가 (관리자만)
st.markdown("---")
if is_admin:
    st.subheader("새 레시피 추가")
    with st.form("add_form"):
        a_name = st.text_input("요리명")
        a_main = st.text_input("주재료")
        a_sub = st.text_input("부재료 (선택)")
        a_method = st.text_area("조리법")
        a_desc = st.text_area("상세설명 (선택)")
        a_date = st.text_input("데이터기준일자 (YYYY-MM-DD, 선택)")
        add_submitted = st.form_submit_button("추가")
        if add_submitted:
            try:
                date_parsed = None
                if a_date:
                    date_parsed = datetime.strptime(a_date, "%Y-%m-%d").date()
                add_recipe(session,
                           name=a_name,
                           main_ingredients=a_main,
                           sub_ingredients=a_sub or None,
                           method=a_method,
                           description=a_desc or None,
                           source_date=date_parsed)
                st.success("레시피 추가 완료")
            except Exception as e:
                st.error(f"추가 실패: {e}")
else:
    st.info("레시피 추가는 관리자만 가능합니다.")

# CSV 내보내기: 현재 필터 결과를 다운로드
st.markdown("---")
st.subheader("데이터 내보내기")
csv = df.to_csv(index=False).encode('utf-8-sig')
st.download_button("현재 결과 CSV 다운로드", data=csv, file_name="recipes_export.csv", mime="text/csv")

session.close()
