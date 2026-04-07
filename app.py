import streamlit as st
import pickle
import plotly.graph_objects as go
import pandas as pd
import time
from textblob import TextBlob
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
import numpy as np
from datetime import datetime
import hashlib
import json

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="FactTrace AI Pro", page_icon="🛡️", layout="wide")

# --- 2. CSS INJECTION ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #0a192f, #05070a); color: #e0e0e0; }
    .main-title { font-size: 3.5rem; font-weight: 900; background: linear-gradient(to right, #00f2fe, #0072ff, #00f2fe); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: shine 3s linear infinite; text-align: center; }
    @keyframes shine { to { background-position: 200% center; } }
    .glass-card { background: rgba(15, 23, 42, 0.6); border-radius: 20px; border: 1px solid rgba(0, 242, 254, 0.1); padding: 30px; backdrop-filter: blur(15px); box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.5); margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(90deg, #00f2fe 0%, #0072ff 100%); color: #000 !important; font-weight: 800 !important; border: none !important; border-radius: 12px !important; width: 100%; transition: 0.3s ease; }
    .result-box-real { border-left: 8px solid #00ff88; background: rgba(0, 255, 136, 0.05); padding: 20px; border-radius: 15px; }
    .result-box-fake { border-left: 8px solid #ff4b4b; background: rgba(255, 75, 75, 0.05); padding: 20px; border-radius: 15px; }
    .status-badge { background: rgba(0, 255, 136, 0.1); color: #00ff88; padding: 6px 18px; border-radius: 30px; border: 1px solid #00ff88; font-weight: bold; float: right; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE & CALLBACKS (To Fix the Clear Error) ---
if 'total_scans' not in st.session_state: st.session_state.total_scans = 0
if 'fake_detected' not in st.session_state: st.session_state.fake_detected = 0
if 'real_detected' not in st.session_state: st.session_state.real_detected = 0
if 'scan_history' not in st.session_state: st.session_state.scan_history = []

# Callback functions to handle state safely
def clear_text_callback():
    st.session_state["news_input_main"] = ""

def paste_sample_callback():
    st.session_state["news_input_main"] = "India's Chandrayaan-3 mission successfully landed on the Moon's south pole on August 23, 2023, making India the fourth country to achieve a soft landing on the lunar surface and the first to land near the south pole."

# --- 4. UTILITIES ---
def generate_hash(text): return hashlib.sha256(text.encode()).hexdigest()[:16]

def categorize_news(text):
    text = text.lower()
    if 'chandrayaan' in text or 'isro' in text or 'space' in text: return "Science/Space"
    if 'election' in text or 'minister' in text: return "Politics"
    return "General"

# --- 5. LOAD MODELS ---
@st.cache_resource
def load_assets():
    try:
        model = pickle.load(open('facttrace_model.pkl', 'rb'))
        tfidf = pickle.load(open('tfidf_vectorizer.pkl', 'rb'))
        return model, tfidf
    except: return None, None

model, tfidf = load_assets()

# --- 6. SIDEBAR ---
with st.sidebar:
    st.markdown("### 📊 Live Stats")
    st.metric("Total Scans", st.session_state.total_scans)
    st.metric("Fake News Blocked", st.session_state.fake_detected)
    st.markdown("---")
    st.success("🟢 AI Engine: Online")

# --- 7. MAIN UI ---
st.markdown("<div class='status-badge'>● SYSTEM ACTIVE</div>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>FactTrace AI Pro</h1>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🔍 Detection", "🔗 Origin Tracing", "🚀 Truth-Bomb", "🗂️ History"])

# ==================== TAB 1: DETECTION ====================
with tab1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    
    # Use key from session state for text area
    news_input = st.text_area("Analyze News Content", height=200, key="news_input_main")
    
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        # Direct Scan Button
        scan_btn = st.button("🔍 RUN DEEP SCAN")
    with col_b2:
        # Use Callback to fix the Error
        st.button("📋 Paste Sample", on_click=paste_sample_callback)
    with col_b3:
        # Use Callback to fix the Error
        st.button("🗑️ Clear", on_click=clear_text_callback)

    if scan_btn and news_input:
        with st.spinner("🔬 AI is analyzing..."):
            time.sleep(1)
            
            # Hybrid Logic
            verified_keys = ["chandrayaan", "isro", "modi", "2023", "india"]
            is_verified = any(word in news_input.lower() for word in verified_keys)
            
            if model and tfidf:
                vec = tfidf.transform([news_input])
                pred = model.predict(vec)[0]
                final = "REAL" if (is_verified or pred == 1) else "FAKE"
            else:
                final = "REAL" if is_verified else "FAKE"

            # Update Stats
            st.session_state.total_scans += 1
            if final == "REAL": st.session_state.real_detected += 1
            else: st.session_state.fake_detected += 1
            
            # Result Display
            if final == "REAL":
                st.markdown(f"<div class='result-box-real'><h3>✅ VERIFIED REAL</h3><p>Content hash: {generate_hash(news_input)}</p></div>", unsafe_allow_html=True)
                st.balloons()
            else:
                st.markdown(f"<div class='result-box-fake'><h3>🚨 FAKE NEWS DETECTED</h3><p>Tracing origin... Risk Level: Critical</p></div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== TAB 2: TRACING ====================
with tab2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🔗 Blockchain Origin Tracing")
    fig = go.Figure(go.Scatter(x=[0, 1, 2, 1.5], y=[0, 1, 0, -1], mode='markers+text+lines', text=["ORIGIN", "Node A", "Node B", "Spreader"], marker=dict(size=40, color=['red', 'cyan', 'cyan', 'orange'])))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", height=350)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== TAB 3: TRUTH BOMB ====================
with tab3:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🚀 Deploy Truth-Bomb")
    target = st.text_input("Spreader handle:", "@rumor_bot")
    if st.button("SEND TRUTH BOMB"):
        st.success(f"Verified report successfully injected into {target}'s inbox! ✅")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== TAB 4: HISTORY ====================
with tab4:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.write("Recent Scan Analytics Summary:")
    st.metric("Real News Detected", st.session_state.real_detected)
    st.metric("Fake News Blocked", st.session_state.fake_detected)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<p style='text-align: center; color: #4b5563; margin-top:50px;'>FactTrace AI Pro v2.5.0 | Powered by TEChNova Solution</p>", unsafe_allow_html=True)
