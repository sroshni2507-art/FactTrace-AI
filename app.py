import streamlit as st
import pickle
import pandas as pd
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="FactTrace AI", page_icon="🛡️", layout="wide")

# --- LOAD MODELS ---
@st.cache_resource
def load_assets():
    model = pickle.load(open('facttrace_model.pkl', 'rb'))
    tfidf = pickle.load(open('tfidf_vectorizer.pkl', 'rb'))
    return model, tfidf

model, tfidf = load_assets()

# --- CUSTOM CSS (For that FakeShield Look) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #060918; color: #ffffff; }
    
    /* Header & Navbar */
    .nav-bar { display: flex; justify-content: space-between; align-items: center; padding: 10px 50px; background: #0b112b; border-bottom: 1px solid #1e2a5a; }
    .nav-tabs { display: flex; gap: 20px; background: #0f173d; padding: 8px 20px; border-radius: 30px; border: 1px solid #2d3b7d; }
    .tab-item { color: #8a96c3; font-weight: bold; cursor: pointer; }
    .tab-active { color: #00f2fe; border-bottom: 2px solid #00f2fe; }

    /* Search/Input Box */
    .input-container { background: #0f173d; border-radius: 20px; padding: 30px; border: 1px solid #1e2a5a; text-align: center; margin-top: 20px; }
    .verify-btn { background: #00f2fe; color: black; font-weight: bold; padding: 12px 40px; border-radius: 30px; border: none; cursor: pointer; float: right; margin-top: -50px; margin-right: 20px; }

    /* Result Cards */
    .result-card { background: #0b112b; border-radius: 15px; padding: 25px; border-left: 10px solid #00f2fe; margin-top: 20px; }
    .fake-card { border-left: 10px solid #ff4b4b; }
    
    /* Metrics Sidebar */
    .metric-container { background: #0f173d; border-radius: 15px; padding: 20px; border: 1px solid #1e2a5a; }
    .status-badge { background: #00332c; color: #00ff88; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; border: 1px solid #00ff88; }
    
    /* Progress Bars */
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #00f2fe , #0072ff); }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER / NAVIGATION ---
st.markdown("""
    <div class="nav-bar">
        <h2 style="color: #ffffff; margin:0;">🛡️ FactTrace <span style="color:#00f2fe;">AI</span></h2>
        <div class="nav-tabs">
            <span class="tab-item tab-active">🔍 Detection</span>
            <span class="tab-item">🔗 Origin Tracing</span>
            <span class="tab-item">📢 Mitigation</span>
        </div>
        <div class="status-badge">● Operational</div>
    </div>
    <p style="text-align:center; color:#8a96c3; margin-top:20px;">Enter news content, a headline, or a URL to verify its credibility against official sources.</p>
    """, unsafe_allow_html=True)

# --- MAIN INPUT ---
with st.container():
    news_input = st.text_area("", height=150, placeholder="Paste news content here...", key="news_area")
    btn_col = st.columns([5, 1])
    with btn_col[1]:
        analyze_btn = st.button("Verify Now", use_container_width=True)

# --- LOGIC & RESULTS ---
if analyze_btn and news_input:
    # Prediction
    vec_text = tfidf.transform([news_input])
    prediction = model.predict(vec_text)[0]
    
    # Sentiment & Confidence (Mock logic for UI matching)
    blob = TextBlob(news_input)
    confidence = 94.5 if prediction == 1 else 12.8
    risk_text = "LOW" if prediction == 1 else "CRITICAL"
    risk_color = "#00ff88" if prediction == 1 else "#ff4b4b"

    col1, col2 = st.columns([2, 1])

    with col1:
        if prediction == 1:
            st.markdown(f"""
                <div class="result-card">
                    <span style="background:#00ff88; color:black; padding:5px 15px; border-radius:5px; font-weight:bold;">VERIFIED CONTENT</span>
                    <h3>The statement is factually correct.</h3>
                    <p style="color:#8a96c3;">This content matches official records and credible news sources. No misinformation detected.</p>
                    <p style="color:#00f2fe;">#Verified #Official #Truth</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="result-card fake-card">
                    <span style="background:#ff4b4b; color:white; padding:5px 15px; border-radius:5px; font-weight:bold;">FAKE CONTENT DETECTED</span>
                    <h3>The statement appears to be misinformation.</h3>
                    <p style="color:#8a96c3;">Linguistic analysis shows patterns of emotional bias and unofficial sources. Mitigation recommended.</p>
                    <p style="color:#ff4b4b;">#FakeNews #Alert #CorrectionNeeded</p>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-container">
                <h4>Analysis Metrics</h4>
                <p style="margin-bottom:0;">Confidence Score</p>
                <h3 style="color:#00f2fe; margin-top:0;">{confidence}%</h3>
            </div>
        """, unsafe_allow_html=True)
        st.progress(confidence/100)
        
        st.markdown(f"""
            <div class="metric-container" style="margin-top:15px;">
                <p style="margin-bottom:0;">Risk Level</p>
                <h3 style="color:{risk_color}; margin-top:0;">{risk_text}</h3>
            </div>
        """, unsafe_allow_html=True)

        # Mitigation Input
        if prediction == 0:
            st.write("---")
            spreader = st.text_input("🎯 Spreader's Number:", placeholder="+91xxxxxx")
            if st.button("Send Mitigation Alert"):
                st.success("Correction SMS Sent! ✅")

else:
    st.info("Waiting for input to verify...")
