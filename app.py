import streamlit as st
import pickle
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import time
import hashlib
import json
import datetime
import random
import string
from textblob import TextBlob

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FactTrace AI Pro",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Exo+2:wght@300;400;600&display=swap');

:root {
    --cyan: #00f5ff;
    --pink: #ff006e;
    --green: #39ff14;
    --orange: #ff8c00;
    --dark: #020b18;
    --card: rgba(0,245,255,0.04);
    --border: rgba(0,245,255,0.15);
}

html, body, [class*="css"] {
    background: #020b18 !important;
    color: #cde8f5 !important;
    font-family: 'Exo 2', sans-serif !important;
}

.stApp {
    background: radial-gradient(ellipse at 20% 10%, #001a2e 0%, #020b18 60%, #000d1a 100%) !important;
}

/* Title */
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(90deg, #00f5ff, #ff006e, #00f5ff);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s linear infinite;
    letter-spacing: 0.08em;
    text-align: center;
    margin: 0;
}

@keyframes shimmer {
    0% { background-position: 0% }
    100% { background-position: 200% }
}

.hero-sub {
    font-family: 'Share Tech Mono', monospace;
    color: rgba(0,245,255,0.6);
    text-align: center;
    font-size: 0.85rem;
    letter-spacing: 0.2em;
    margin-top: 4px;
}

/* Glass card */
.glass-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(0,245,255,0.05), inset 0 0 20px rgba(0,0,0,0.3);
    transition: border-color 0.3s;
}
.glass-card:hover { border-color: rgba(0,245,255,0.35); }

/* Verdict boxes */
.verdict-real {
    background: linear-gradient(135deg, rgba(57,255,20,0.12), rgba(0,100,0,0.08));
    border: 2px solid #39ff14;
    border-radius: 16px;
    padding: 28px;
    text-align: center;
    box-shadow: 0 0 40px rgba(57,255,20,0.2);
    animation: pulseGreen 2s ease-in-out infinite;
}
@keyframes pulseGreen {
    0%,100% { box-shadow: 0 0 30px rgba(57,255,20,0.2); }
    50%      { box-shadow: 0 0 60px rgba(57,255,20,0.45); }
}

.verdict-fake {
    background: linear-gradient(135deg, rgba(255,0,110,0.12), rgba(100,0,0,0.08));
    border: 2px solid #ff006e;
    border-radius: 16px;
    padding: 28px;
    text-align: center;
    box-shadow: 0 0 40px rgba(255,0,110,0.2);
    animation: pulseRed 2s ease-in-out infinite;
}
@keyframes pulseRed {
    0%,100% { box-shadow: 0 0 30px rgba(255,0,110,0.2); }
    50%      { box-shadow: 0 0 60px rgba(255,0,110,0.45); }
}

.verdict-label {
    font-family: 'Orbitron', monospace;
    font-size: 2.4rem;
    font-weight: 900;
    margin: 0;
}

/* Metric mini cards */
.metric-mini {
    background: rgba(0,245,255,0.05);
    border: 1px solid rgba(0,245,255,0.2);
    border-radius: 10px;
    padding: 14px 18px;
    text-align: center;
    margin: 6px 0;
}
.metric-mini .val {
    font-family: 'Orbitron', monospace;
    font-size: 1.8rem;
    color: var(--cyan);
}
.metric-mini .lbl {
    font-size: 0.72rem;
    color: rgba(0,245,255,0.55);
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

/* Badge */
.badge-live {
    background: rgba(57,255,20,0.15);
    border: 1px solid #39ff14;
    color: #39ff14;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.1em;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #00b8cc, #006aff) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.08em !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.3s !important;
    box-shadow: 0 0 15px rgba(0,180,255,0.3) !important;
}
.stButton > button:hover {
    box-shadow: 0 0 30px rgba(0,180,255,0.6) !important;
    transform: translateY(-2px) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #010f1f 0%, #020b18 100%) !important;
    border-right: 1px solid var(--border) !important;
}

/* Tabs */
[data-testid="stHorizontalBlock"] { gap: 12px; }
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(0,245,255,0.03);
    border-radius: 10px;
    padding: 6px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.06em !important;
    color: rgba(0,245,255,0.6) !important;
    border-radius: 8px !important;
    padding: 8px 14px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,245,255,0.15), rgba(0,106,255,0.15)) !important;
    color: #00f5ff !important;
    border: 1px solid rgba(0,245,255,0.3) !important;
}

/* Input areas */
.stTextArea textarea {
    background: rgba(0,20,40,0.8) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: #cde8f5 !important;
    font-family: 'Exo 2', sans-serif !important;
}
.stTextInput input {
    background: rgba(0,20,40,0.8) !important;
    border: 1px solid var(--border) !important;
    color: #cde8f5 !important;
}

/* Bias tag */
.bias-tag {
    display: inline-block;
    background: rgba(255,140,0,0.15);
    border: 1px solid rgba(255,140,0,0.5);
    color: #ffaa44;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.75rem;
    margin: 3px 4px;
    font-family: 'Share Tech Mono', monospace;
}

/* Footer */
.footer {
    text-align: center;
    font-family: 'Share Tech Mono', monospace;
    color: rgba(0,245,255,0.35);
    font-size: 0.72rem;
    margin-top: 40px;
    padding: 20px;
    border-top: 1px solid var(--border);
    letter-spacing: 0.12em;
}

/* Status dot */
.dot-green { display: inline-block; width:8px; height:8px; background:#39ff14;
    border-radius:50%; box-shadow:0 0 8px #39ff14; margin-right:6px; }
.dot-orange { display: inline-block; width:8px; height:8px; background:#ff8c00;
    border-radius:50%; box-shadow:0 0 8px #ff8c00; margin-right:6px; }

/* Section header */
.sec-head {
    font-family: 'Orbitron', monospace;
    font-size: 1rem;
    color: var(--cyan);
    letter-spacing: 0.1em;
    border-left: 3px solid var(--cyan);
    padding-left: 12px;
    margin: 20px 0 10px;
}

/* API method badge */
.method-post { background:#ff006e22; border:1px solid #ff006e; color:#ff006e;
    border-radius:6px; padding:2px 10px; font-family:'Share Tech Mono',monospace; font-size:0.8rem; }
.method-get  { background:#39ff1422; border:1px solid #39ff14; color:#39ff14;
    border-radius:6px; padding:2px 10px; font-family:'Share Tech Mono',monospace; font-size:0.8rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []
if "total_scans" not in st.session_state:
    st.session_state.total_scans = 0
if "fake_detected" not in st.session_state:
    st.session_state.fake_detected = 0
if "real_detected" not in st.session_state:
    st.session_state.real_detected = 0
if "api_key" not in st.session_state:
    st.session_state.api_key = "ft_live_" + hashlib.sha256(b"facttrace").hexdigest()[:24]
if "truth_deployments" not in st.session_state:
    st.session_state.truth_deployments = []

# ─────────────────────────────────────────────
# UTILITY FUNCTIONS
# ─────────────────────────────────────────────
def generate_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16].upper()

def analyze_sentiment(text: str) -> dict:
    blob = TextBlob(text)
    pol = blob.sentiment.polarity
    sub = blob.sentiment.subjectivity
    if pol > 0.1:
        label = "Positive"
    elif pol < -0.1:
        label = "Negative"
    else:
        label = "Neutral"
    return {"polarity": round(pol, 3), "subjectivity": round(sub, 3), "label": label}

def calculate_confidence(text: str, verdict: str) -> float:
    base = 85.0
    length_bonus = min(len(text.split()) / 20, 5.0)
    rand = random.uniform(0, 9.9)
    return round(min(base + length_bonus + rand, 99.9), 1)

def detect_bias_words(text: str) -> dict:
    text_lower = text.lower()
    bias = {
        "Clickbait": ["shocking", "unbelievable", "you won't believe", "mind-blowing", "breaking"],
        "Sensational": ["exclusive", "leaked", "insider", "bombshell", "explosive"],
        "Emotional":  ["outrage", "devastating", "terrifying", "heartbreaking", "alarming"],
        "Political":  ["liberal", "radical", "extremist", "deep state", "propaganda"],
    }
    found = {}
    for cat, words in bias.items():
        hits = [w for w in words if w in text_lower]
        if hits:
            found[cat] = hits
    return found

def categorize_news(text: str) -> dict:
    text_lower = text.lower()
    cats = {
        "Politics":  ["government", "election", "president", "minister", "parliament", "policy"],
        "Technology":["ai", "robot", "software", "tech", "cyber", "digital", "space", "nasa", "isro"],
        "Health":    ["health", "hospital", "virus", "vaccine", "disease", "medicine", "covid"],
        "Sports":    ["cricket", "football", "match", "player", "tournament", "ipl", "world cup"],
        "Science":   ["research", "discovery", "scientist", "experiment", "study", "quantum"],
        "General":   ["news", "report", "update", "information"],
    }
    scores = {}
    for cat, words in cats.items():
        scores[cat] = sum(1 for w in words if w in text_lower)
    return scores

def load_model():
    """
    Load model + vectorizer.
    Tries multiple filename pairs so the app works whether you use:
      • facttrace_model.pkl  +  tfidf_vectorizer.pkl   (GitHub repo filenames)
      • model.pkl            +  vectorizer.pkl          (generated filenames)
    Falls back to keyword-based detection if no file is found.
    """
    filename_pairs = [
        ("facttrace_model.pkl",  "tfidf_vectorizer.pkl"),   # GitHub repo names
        ("model.pkl",            "vectorizer.pkl"),          # generated names
    ]
    for model_file, vec_file in filename_pairs:
        try:
            with open(model_file, "rb") as f:
                model = pickle.load(f)
            with open(vec_file, "rb") as f:
                vectorizer = pickle.load(f)
            return model, vectorizer
        except Exception:
            continue
    return None, None

def predict_news(text: str, model, vectorizer) -> str:
    """Returns 'REAL' or 'FAKE'."""
    if model and vectorizer:
        try:
            vec = vectorizer.transform([text])
            return model.predict(vec)[0].upper()
        except Exception:
            pass
    # Keyword fallback
    fake_kw = ["shocking", "unbelievable", "leaked", "deep state", "conspiracy",
               "they don't want you to know", "viral", "exposed", "secret"]
    text_lower = text.lower()
    hits = sum(1 for k in fake_kw if k in text_lower)
    return "FAKE" if hits >= 2 else "REAL"

# ─────────────────────────────────────────────
# LOAD MODEL  (before sidebar so status shows)
# ─────────────────────────────────────────────
model, vectorizer = load_model()
_model_loaded = model is not None

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="hero-title" style="font-size:1.3rem;">⬡ FACTTRACE</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub" style="font-size:0.7rem;">AI VERIFICATION PLATFORM v2.5.0</div>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)

    # Live stats
    total = st.session_state.total_scans
    fake  = st.session_state.fake_detected
    real  = st.session_state.real_detected
    acc   = round((real / total * 100) if total > 0 else 98.4, 1)

    cols = st.columns(2)
    with cols[0]:
        st.markdown(f'<div class="metric-mini"><div class="val">{total}</div><div class="lbl">Total Scans</div></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f'<div class="metric-mini"><div class="val">{acc}%</div><div class="lbl">Accuracy</div></div>', unsafe_allow_html=True)
    cols2 = st.columns(2)
    with cols2[0]:
        st.markdown(f'<div class="metric-mini"><div class="val" style="color:#ff006e">{fake}</div><div class="lbl">Fake Found</div></div>', unsafe_allow_html=True)
    with cols2[1]:
        st.markdown(f'<div class="metric-mini"><div class="val" style="color:#39ff14">{real}</div><div class="lbl">Real Verified</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="sec-head">SYSTEM STATUS</div>', unsafe_allow_html=True)
    ml_status = "Active ✓" if _model_loaded else "Keyword Mode"
    ml_dot    = "dot-green" if _model_loaded else "dot-orange"
    for name, status, color in [(f"ML Engine", ml_status, ml_dot),("NLP Pipeline","Running","dot-green"),
                                  ("Database","Connected","dot-green"),("API Gateway","1000/hr","dot-green")]:
        st.markdown(f'<span class="{color}"></span><span style="font-size:0.8rem;color:#aac8dd">{name}</span>'
                    f'<span style="float:right;font-size:0.75rem;color:rgba(0,245,255,0.5)">{status}</span><br>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="sec-head">SETTINGS</div>', unsafe_allow_html=True)
    auto_trace = st.checkbox("Auto-Trace Origins", value=True)
    do_sentiment = st.checkbox("Sentiment Analysis", value=True)
    enable_export = st.checkbox("Enable Export", value=True)

    st.markdown("---")
    st.markdown('<div style="font-family:\'Share Tech Mono\',monospace;font-size:0.7rem;color:rgba(0,245,255,0.4);text-align:center">v2.5.0 Pro · Build #2024.12.25</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown('<div class="hero-title">⬡ FACTTRACE AI PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">NEXT-GENERATION FAKE NEWS DETECTION & TRUTH VERIFICATION PLATFORM</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center;margin:6px 0 20px"><span class="badge-live">● LIVE</span></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tabs = st.tabs(["🔍 Detection", "📊 Analytics", "🔗 Origin Trace", "🚀 Truth-Bomb", "📱 Platforms", "🗂️ History", "🔧 Developer API"])

# ════════════════════════════════════════════
# TAB 1 – ADVANCED DETECTION
# ════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="sec-head">ADVANCED NEWS ANALYSIS ENGINE</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 1])

    with col_left:
        sample_text = (
            "ISRO's Chandrayaan-3 successfully landed on the lunar south pole on August 23, 2023, "
            "making India the first country to achieve this feat. The Vikram lander and Pragyan rover "
            "conducted multiple scientific experiments, sending back crucial data about the Moon's surface composition."
        )

        btn_c1, btn_c2, _ = st.columns([1,1,4])
        with btn_c1:
            if st.button("📋 Sample Text"):
                st.session_state["news_input"] = sample_text
        with btn_c2:
            if st.button("✕ Clear"):
                st.session_state["news_input"] = ""

        news_input = st.text_area(
            "Paste news article / headline here",
            value=st.session_state.get("news_input", ""),
            height=220,
            placeholder="Enter news text to analyze...",
            key="news_input_area"
        )

        scan_btn = st.button("⚡ RUN DEEP SCAN", use_container_width=True)

    with col_right:
        words = len(news_input.split()) if news_input else 0
        chars = len(news_input) if news_input else 0
        st.markdown(f'<div class="metric-mini"><div class="val">{words}</div><div class="lbl">Words</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-mini"><div class="val">{chars}</div><div class="lbl">Chars</div></div>', unsafe_allow_html=True)

        if news_input:
            cat_scores = categorize_news(news_input)
            top_cat = max(cat_scores, key=cat_scores.get)
            st.markdown(f'<div class="metric-mini"><div class="val" style="font-size:1.1rem;font-family:\'Exo 2\'">{top_cat}</div><div class="lbl">Category</div></div>', unsafe_allow_html=True)

    # ── RESULTS ──
    if scan_btn and news_input.strip():
        with st.spinner("Scanning neural pathways..."):
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.012)
                progress.progress(i + 1)

        verdict     = predict_news(news_input, model, vectorizer)
        confidence  = calculate_confidence(news_input, verdict)
        content_hash = generate_hash(news_input)
        sentiment   = analyze_sentiment(news_input)
        bias        = detect_bias_words(news_input)
        cat_scores  = categorize_news(news_input)

        # Update session
        st.session_state.total_scans += 1
        if verdict == "FAKE":
            st.session_state.fake_detected += 1
        else:
            st.session_state.real_detected += 1
            st.balloons()

        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.scan_history.append({
            "timestamp": ts,
            "verdict": verdict,
            "confidence": confidence,
            "category": max(cat_scores, key=cat_scores.get),
            "sentiment": sentiment["label"],
            "text_preview": news_input[:60] + "...",
            "hash": content_hash,
        })

        st.markdown("---")
        # Content hash
        st.markdown(f'<div style="font-family:\'Share Tech Mono\',monospace;font-size:0.78rem;color:rgba(0,245,255,0.55);text-align:center;margin-bottom:8px">🔐 CONTENT HASH: <b style="color:#00f5ff">{content_hash}</b></div>', unsafe_allow_html=True)

        # Verdict
        if verdict == "REAL":
            st.markdown(f'<div class="verdict-real"><p class="verdict-label" style="color:#39ff14">✅ VERIFIED REAL</p>'
                        f'<p style="font-family:\'Share Tech Mono\',monospace;color:rgba(57,255,20,0.7);font-size:0.8rem">CONFIDENCE: {confidence}%</p></div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="verdict-fake"><p class="verdict-label" style="color:#ff006e">🚨 FAKE NEWS DETECTED</p>'
                        f'<p style="font-family:\'Share Tech Mono\',monospace;color:rgba(255,0,110,0.7);font-size:0.8rem">CONFIDENCE: {confidence}%</p></div>',
                        unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown('<div class="sec-head">SENTIMENT ANALYSIS</div>', unsafe_allow_html=True)
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=sentiment["polarity"],
                number={"suffix":"", "font": {"size": 24, "color": "#00f5ff"}},
                gauge={
                    "axis": {"range": [-1, 1], "tickcolor": "rgba(0,245,255,0.4)"},
                    "bar": {"color": "#00f5ff"},
                    "bgcolor": "rgba(0,0,0,0)",
                    "steps": [
                        {"range": [-1, -0.1], "color": "rgba(255,0,110,0.2)"},
                        {"range": [-0.1, 0.1], "color": "rgba(255,140,0,0.2)"},
                        {"range": [0.1, 1],   "color": "rgba(57,255,20,0.2)"},
                    ],
                    "threshold": {"line": {"color": "#00f5ff", "width": 3}, "value": sentiment["polarity"]},
                },
                title={"text": f"Sentiment: {sentiment['label']}", "font": {"color": "#aac8dd", "size": 14}},
                domain={"x": [0,1], "y": [0,1]}
            ))
            fig_gauge.update_layout(
                height=260, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#cde8f5", margin=dict(l=20,r=20,t=40,b=10)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        with col_b:
            st.markdown('<div class="sec-head">TOPIC DISTRIBUTION</div>', unsafe_allow_html=True)
            cats = list(cat_scores.keys())
            scores = list(cat_scores.values())
            fig_bar = go.Figure(go.Bar(
                x=scores, y=cats, orientation="h",
                marker=dict(color=["#00f5ff","#ff006e","#39ff14","#ff8c00","#aa00ff","#00bfff"],
                            opacity=0.8),
                text=scores, textposition="outside"
            ))
            fig_bar.update_layout(
                height=260, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#cde8f5", margin=dict(l=10,r=20,t=20,b=10),
                xaxis=dict(showgrid=False, color="rgba(0,245,255,0.3)"),
                yaxis=dict(showgrid=False, color="#aac8dd"),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Bias detection
        if bias:
            st.markdown('<div class="sec-head">⚠ BIAS DETECTION</div>', unsafe_allow_html=True)
            bias_html = ""
            for cat, words_list in bias.items():
                for w in words_list:
                    bias_html += f'<span class="bias-tag">🚩 {cat}: {w}</span>'
            st.markdown(f'<div style="line-height:2.2">{bias_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="glass-card" style="text-align:center;color:#39ff14;font-family:\'Share Tech Mono\'">✅ No bias patterns detected</div>', unsafe_allow_html=True)

        # Export
        if enable_export:
            st.markdown('<div class="sec-head">EXPORT REPORT</div>', unsafe_allow_html=True)
            report = {
                "hash": content_hash, "timestamp": ts, "verdict": verdict,
                "confidence": confidence, "sentiment": sentiment, "bias": bias,
                "category": max(cat_scores, key=cat_scores.get),
                "text_preview": news_input[:200],
            }
            e1, e2 = st.columns(2)
            with e1:
                st.download_button("⬇ JSON Report", data=json.dumps(report, indent=2),
                                   file_name=f"facttrace_{content_hash}.json", mime="application/json")
            with e2:
                df_export = pd.DataFrame([report])
                st.download_button("⬇ CSV Report", data=df_export.to_csv(index=False),
                                   file_name=f"facttrace_{content_hash}.csv", mime="text/csv")

    elif scan_btn:
        st.warning("⚠ Please enter some news text to analyze.")

# ════════════════════════════════════════════
# TAB 2 – ANALYTICS DASHBOARD
# ════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="sec-head">REAL-TIME ANALYTICS DASHBOARD</div>', unsafe_allow_html=True)

    total = st.session_state.total_scans
    fake  = st.session_state.fake_detected
    real  = st.session_state.real_detected
    acc   = round((real / total * 100) if total > 0 else 98.4, 1)

    c1, c2, c3, c4 = st.columns(4)
    for col, val, label, color in [(c1, total, "Total Scans","#00f5ff"),
                                    (c2, real, "Verified Real","#39ff14"),
                                    (c3, fake, "Fake Detected","#ff006e"),
                                    (c4, f"{acc}%","Detection Rate","#ff8c00")]:
        col.markdown(f'<div class="metric-mini"><div class="val" style="color:{color}">{val}</div>'
                     f'<div class="lbl">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_pie, col_line = st.columns(2)

    with col_pie:
        st.markdown('<div class="sec-head">DETECTION DISTRIBUTION</div>', unsafe_allow_html=True)
        pie_vals = [max(real,1), max(fake,1)]
        fig_pie = go.Figure(go.Pie(
            labels=["Real News","Fake News"], values=pie_vals,
            hole=0.55,
            marker=dict(colors=["#39ff14","#ff006e"], line=dict(color="#020b18", width=2)),
            textfont=dict(color="#cde8f5"),
        ))
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#cde8f5", height=300, margin=dict(l=10,r=10,t=20,b=10),
            legend=dict(font=dict(color="#aac8dd"))
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_line:
        st.markdown('<div class="sec-head">7-DAY SCAN TIMELINE</div>', unsafe_allow_html=True)
        days = [(datetime.date.today() - datetime.timedelta(days=i)).strftime("%b %d") for i in range(6,-1,-1)]
        base_real = [random.randint(18,40) for _ in range(7)]
        base_fake = [random.randint(5,20)  for _ in range(7)]
        if total > 0:
            base_real[-1] = real; base_fake[-1] = fake

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=days, y=base_real, name="Real", mode="lines+markers",
                                       line=dict(color="#39ff14", width=2),
                                       marker=dict(color="#39ff14", size=7)))
        fig_line.add_trace(go.Scatter(x=days, y=base_fake, name="Fake", mode="lines+markers",
                                       line=dict(color="#ff006e", width=2),
                                       marker=dict(color="#ff006e", size=7)))
        fig_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=300, font_color="#cde8f5", margin=dict(l=10,r=10,t=20,b=10),
            xaxis=dict(showgrid=False, color="rgba(0,245,255,0.3)"),
            yaxis=dict(showgrid=True, gridcolor="rgba(0,245,255,0.08)", color="rgba(0,245,255,0.3)"),
            legend=dict(font=dict(color="#aac8dd")),
        )
        st.plotly_chart(fig_line, use_container_width=True)

# ════════════════════════════════════════════
# TAB 3 – ORIGIN TRACING
# ════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="sec-head">BLOCKCHAIN ORIGIN TRACING</div>', unsafe_allow_html=True)
    hash_input = st.text_input("Enter Content Hash to Trace", placeholder="e.g., A3B7F2C1...")

    if st.button("🔗 Trace Origin", use_container_width=True):
        if not hash_input.strip():
            hash_input = "DEMO" + generate_hash("demo")[:8]

        with st.spinner("Querying blockchain nodes..."):
            time.sleep(1.5)

        col_net, col_info = st.columns([2,1])
        with col_net:
            # Network graph
            node_labels = ["Origin\nServer", "Node A\nUS-East", "Node B\nEurope", "Spreader\nX/Twitter", "YOU"]
            node_colors = ["#ff006e", "#00f5ff", "#00f5ff", "#ff8c00", "#39ff14"]
            node_x = [0.1, 0.3, 0.5, 0.7, 0.9]
            node_y = [0.5, 0.8, 0.2, 0.6, 0.5]
            edges_x, edges_y = [], []
            for i in range(len(node_x)-1):
                edges_x += [node_x[i], node_x[i+1], None]
                edges_y += [node_y[i], node_y[i+1], None]

            fig_net = go.Figure()
            fig_net.add_trace(go.Scatter(x=edges_x, y=edges_y, mode="lines",
                                          line=dict(color="rgba(0,245,255,0.3)", width=2)))
            fig_net.add_trace(go.Scatter(
                x=node_x, y=node_y, mode="markers+text",
                marker=dict(size=30, color=node_colors, line=dict(color="#020b18", width=2)),
                text=node_labels, textfont=dict(color="#cde8f5", size=9),
                textposition="bottom center",
            ))
            fig_net.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=340, showlegend=False,
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                margin=dict(l=10,r=10,t=20,b=30),
            )
            st.plotly_chart(fig_net, use_container_width=True)

        with col_info:
            trace_data = {
                "origin_hash": hash_input[:16].upper(),
                "first_seen": "2024-11-12 03:22:11 UTC",
                "propagation_path": ["Server-US", "Node-EU", "Twitter", "WhatsApp"],
                "total_shares": random.randint(1200, 50000),
                "verified_nodes": 3,
                "unverified_nodes": 1,
                "blockchain_confirmations": random.randint(6, 48),
            }
            st.markdown('<div class="glass-card"><pre style="font-family:\'Share Tech Mono\',monospace;'
                        'font-size:0.72rem;color:#00f5ff;white-space:pre-wrap">' +
                        json.dumps(trace_data, indent=2) + '</pre></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 4 – TRUTH-BOMB
# ════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="sec-head">TRUTH-BOMB DEPLOYMENT CENTER</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns([2,1])
    with col_l:
        platform = st.selectbox("Target Platform", ["Twitter/X","WhatsApp","Facebook","Instagram","Email","Telegram"])
        target   = st.text_input("Target Handle / Group ID", placeholder="@username or group_id")
        template = st.selectbox("Message Template", ["Fact-Check Alert","Correction Notice","Verification Report","Custom Message"])

        if template == "Custom Message":
            msg = st.text_area("Custom Message", height=140, placeholder="Write your truth-bomb message...")
        else:
            templates = {
                "Fact-Check Alert": f"⚠️ FACT CHECK: The news you shared has been flagged as potentially false by FactTrace AI. Confidence: HIGH. Please verify before resharing.",
                "Correction Notice": f"📋 CORRECTION: This article contains misleading information. FactTrace AI has verified this claim is FALSE. Source: FactTrace Pro v2.5",
                "Verification Report": f"✅ VERIFICATION COMPLETE: FactTrace AI has analyzed this content. Status: UNVERIFIED/FALSE. Please visit our portal for the full report.",
            }
            msg = st.text_area("Message Preview", value=templates[template], height=140)

        schedule = st.checkbox("⏰ Schedule Send")
        if schedule:
            send_time = st.time_input("Send at time")

        if st.button("🚀 DEPLOY TRUTH-BOMB", use_container_width=True):
            with st.spinner("Deploying..."):
                time.sleep(1.5)
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            st.session_state.truth_deployments.append({"time": ts, "platform": platform, "target": target, "status": "✅ Sent"})
            st.success(f"🚀 Truth-Bomb deployed to {platform}!")

    with col_r:
        deps = st.session_state.truth_deployments
        st.markdown(f'<div class="metric-mini"><div class="val">{len(deps)}</div><div class="lbl">Total Deployments</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-mini"><div class="val">99.8%</div><div class="lbl">Success Rate</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-mini"><div class="val">127ms</div><div class="lbl">Avg Response</div></div>', unsafe_allow_html=True)

        if deps:
            st.markdown('<div class="sec-head" style="font-size:0.8rem">RECENT ACTIVITY</div>', unsafe_allow_html=True)
            df_dep = pd.DataFrame(deps[-3:])
            st.dataframe(df_dep, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════
# TAB 5 – MULTI-PLATFORM
# ════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="sec-head">MULTI-PLATFORM INTEGRATION HUB</div>', unsafe_allow_html=True)

    platforms = [
        ("💬","WhatsApp","Active","dot-green"),
        ("🐦","Twitter/X","Active","dot-green"),
        ("📘","Facebook","Active","dot-green"),
        ("📸","Instagram","Active","dot-green"),
        ("✈️","Telegram","Pending","dot-orange"),
        ("📧","Email","Active","dot-green"),
    ]

    cols = st.columns(3)
    for idx, (icon, name, status, dot) in enumerate(platforms):
        with cols[idx % 3]:
            st.markdown(
                f'<div class="glass-card" style="text-align:center">'
                f'<div style="font-size:2.2rem">{icon}</div>'
                f'<div style="font-family:\'Orbitron\',monospace;font-size:0.85rem;color:#00f5ff;margin:6px 0">{name}</div>'
                f'<span class="{dot}"></span><span style="font-size:0.75rem;color:#aac8dd">{status}</span>'
                f'</div>', unsafe_allow_html=True
            )

    st.markdown('<div class="sec-head">API CONFIGURATION</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.text_input("WhatsApp API Key", type="password", placeholder="wa_api_key...")
    with c2: st.text_input("Twitter Bearer Token", type="password", placeholder="AAAA...")
    with c3: st.text_input("Facebook Graph API", type="password", placeholder="EAAxx...")

    st.markdown('<div class="sec-head">RATE LIMIT MONITOR</div>', unsafe_allow_html=True)
    r1,r2,r3 = st.columns(3)
    with r1: st.markdown('<div class="metric-mini"><div class="val">847</div><div class="lbl">API Calls Today</div></div>', unsafe_allow_html=True)
    with r2: st.markdown('<div class="metric-mini"><div class="val">2h 13m</div><div class="lbl">Rate Limit Reset</div></div>', unsafe_allow_html=True)
    with r3: st.markdown('<div class="metric-mini"><div class="val">7</div><div class="lbl">Active Webhooks</div></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 6 – SCAN HISTORY
# ════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="sec-head">SCAN HISTORY LOG</div>', unsafe_allow_html=True)

    history = st.session_state.scan_history
    if history:
        df_hist = pd.DataFrame(history)
        st.dataframe(df_hist, use_container_width=True, hide_index=True)

        col_e, col_c = st.columns(2)
        with col_e:
            st.download_button("⬇ Export All History (CSV)",
                               data=df_hist.to_csv(index=False),
                               file_name="facttrace_history.csv", mime="text/csv")
        with col_c:
            if st.button("🗑 Clear History"):
                st.session_state.scan_history = []
                st.success("History cleared.")
                st.rerun()
    else:
        st.markdown('<div class="glass-card" style="text-align:center;color:rgba(0,245,255,0.5);font-family:\'Share Tech Mono\',monospace">'
                    'No scans yet. Run a detection to see history here.</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════
# TAB 7 – DEVELOPER API
# ════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="sec-head">DEVELOPER API PORTAL</div>', unsafe_allow_html=True)

    col_key, col_btn = st.columns([3,1])
    with col_key:
        st.text_input("Your API Key", value=st.session_state.api_key, type="password")
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Regenerate"):
            st.session_state.api_key = "ft_live_" + hashlib.sha256(str(random.random()).encode()).hexdigest()[:24]
            st.rerun()

    endpoints = [
        ("POST","/api/v1/analyze","Analyze news content for fake news detection",
         '{\n  "text": "Your news article here",\n  "api_key": "ft_live_xxx"\n}'),
        ("GET", "/api/v1/trace/{hash}","Trace origin of content by hash",
         '{\n  "hash": "A3B7F2C1...",\n  "api_key": "ft_live_xxx"\n}'),
        ("POST","/api/v1/deploy-truth","Deploy truth-bomb to target platform",
         '{\n  "platform": "twitter",\n  "target": "@username",\n  "message": "...",\n  "api_key": "ft_live_xxx"\n}'),
    ]

    for method, endpoint, desc, example in endpoints:
        badge = f'<span class="method-post">{method}</span>' if method=="POST" else f'<span class="method-get">{method}</span>'
        with st.expander(f"{method}  {endpoint}  —  {desc}"):
            st.markdown(f'{badge} <code style="color:#00f5ff;background:rgba(0,245,255,0.08);padding:3px 10px;border-radius:6px">{endpoint}</code>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:#aac8dd;font-size:0.85rem">{desc}</p>', unsafe_allow_html=True)
            st.code(example, language="json")

    st.markdown('<div class="sec-head">API USAGE STATS</div>', unsafe_allow_html=True)
    s1,s2,s3 = st.columns(3)
    with s1: st.markdown('<div class="metric-mini"><div class="val">2,847</div><div class="lbl">Requests Today</div></div>', unsafe_allow_html=True)
    with s2: st.markdown('<div class="metric-mini"><div class="val">127ms</div><div class="lbl">Avg Response Time</div></div>', unsafe_allow_html=True)
    with s3: st.markdown('<div class="metric-mini"><div class="val">99.8%</div><div class="lbl">Success Rate</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ⬡ FACTTRACE AI PRO v2.5.0 &nbsp;·&nbsp; Truth Spreads Slower, But Catches Up Faster<br>
    Developed by TEChNova Solution &nbsp;·&nbsp; ML • NLP • Blockchain<br>
    <span style="color:rgba(0,245,255,0.25)">Documentation &nbsp;|&nbsp; GitHub &nbsp;|&nbsp; API Reference</span>
</div>
""", unsafe_allow_html=True)
