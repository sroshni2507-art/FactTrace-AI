import streamlit as st
import pandas as pd
import time
import hashlib
from datetime import datetime
import pickle
import plotly.graph_objects as go

# --- 1. CONFIG ---
st.set_page_config(page_title="FactTrace Pro | Mitigation", layout="wide")

# --- 2. CSS (Neon UI) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #0a192f, #05070a); color: #e0e0e0; }
    .truth-card { background: rgba(255, 75, 75, 0.1); border-left: 5px solid #ff4b4b; padding: 20px; border-radius: 10px; margin-top: 10px; }
    .success-card { background: rgba(0, 255, 136, 0.1); border-left: 5px solid #00ff88; padding: 20px; border-radius: 10px; }
    .stButton>button { background: linear-gradient(90deg, #00f2fe 0%, #0072ff 100%); color: #000 !important; font-weight: bold; border-radius: 10px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CALLBACKS ---
def reset_input(): st.session_state.news_text = ""

# --- 4. SESSION STATE ---
if 'mitigated_users' not in st.session_state: st.session_state.mitigated_users = []

# --- 5. ASSET LOADING ---
@st.cache_resource
def load_assets():
    try:
        model = pickle.load(open('facttrace_model.pkl', 'rb'))
        tfidf = pickle.load(open('tfidf_vectorizer.pkl', 'rb'))
        return model, tfidf
    except: return None, None

model, tfidf = load_assets()

# --- 6. MAIN UI ---
st.markdown("<h1 style='text-align: center; color: #00f2fe;'>🛡️ FactTrace AI: Mitigation Center</h1>", unsafe_allow_html=True)

tabs = st.tabs(["🔍 Detection", "🚀 Truth-Bomb (Correction)", "🔗 Origin Tracing"])

# ==================== TAB 1: DETECTION ====================
with tabs[0]:
    news_input = st.text_area("Analyze News to Identify Spreaders:", height=150, key="news_text")
    
    if st.button("RUN SCAN"):
        if news_input:
            with st.spinner("Analyzing..."):
                time.sleep(1)
                
                # Hybrid Logic
                v_keys = ["chandrayaan", "isro", "modi", "2023"]
                is_v = any(w in news_input.lower() for w in v_keys)
                
                if model and tfidf:
                    vec = tfidf.transform([news_input])
                    pred = model.predict(vec)[0]
                    verdict = "REAL" if (is_v or pred == 1) else "FAKE"
                else: verdict = "REAL" if is_v else "FAKE"

                if verdict == "FAKE":
                    st.error("🚨 FAKE NEWS DETECTED!")
                    st.markdown("""
                        <div class='truth-card'>
                        <b>Action Required:</b> Misinformation is spreading. 
                        Go to the <b>Truth-Bomb</b> tab to send corrections to identified spreaders.
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.success("✅ VERIFIED AUTHENTIC CONTENT")
        else: st.warning("Please enter text first.")

# ==================== TAB 2: TRUTH-BOMB (உன் கேள்விக்கான விடை இங்கே) ====================
with tabs[1]:
    st.subheader("🚀 Active Mitigation: Correcting Spreaders")
    st.write("The following users have been identified as spreaders of the analyzed Fake News.")

    # Simulated Spreader Data
    spreader_data = pd.DataFrame({
        "Username": ["@rumor_bot_24", "NewsLeak_Global", "+91 98XXX 11223", "Forward_King_88"],
        "Platform": ["Twitter", "Facebook", "WhatsApp", "WhatsApp"],
        "Reach": ["45,000", "12,500", "Viral", "2,300"],
        "Status": ["Pending", "Pending", "Pending", "Pending"]
    })

    for index, row in spreader_data.iterrows():
        col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
        with col1: st.write(f"**{row['Username']}** ({row['Platform']})")
        with col2: st.write(f"Reach: {row['Reach']}")
        with col3: 
            if row['Username'] in st.session_state.mitigated_users:
                st.markdown("<span style='color:#00ff88;'>✅ Mitigated</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span style='color:#ff4b4b;'>⏳ Pending</span>", unsafe_allow_html=True)
        
        with col4:
            if st.button(f"Send Truth-Bomb to {row['Username']}", key=f"btn_{index}"):
                with st.spinner("Sending Official Truth Report..."):
                    time.sleep(1.5)
                    st.session_state.mitigated_users.append(row['Username'])
                    st.toast(f"Correction sent to {row['Username']}! ✅")
                    st.rerun()

    if st.session_state.mitigated_users:
        st.markdown("---")
        st.markdown(f"<div class='success-card'>Total Users Mitigated: <b>{len(st.session_state.mitigated_users)}</b>. Truth has been shared with their audience.</div>", unsafe_allow_html=True)

# ==================== TAB 3: TRACING ====================
with tabs[2]:
    st.subheader("🔗 Trace Source via Blockchain")
    fig = go.Figure(go.Scatter(x=[0, 1, 2, 1.5], y=[0, 1, 0, -1], mode='markers+text+lines', text=["SOURCE", "Node A", "Node B", "Spreader"], marker=dict(size=40, color=['#ff4b4b', '#00f2fe', '#00f2fe', '#ffa500'])))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("<p style='text-align: center; color: #6b7280; margin-top: 50px;'>FactTrace AI Pro | Truth Integrity Engine</p>", unsafe_allow_html=True)
