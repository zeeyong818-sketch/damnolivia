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
      <
