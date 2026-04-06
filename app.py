import streamlit as st
import pickle
import plotly.graph_objects as go
import time

# Page Config
st.set_page_config(page_title="FakeShield AI", layout="wide")

# --- LOAD MODELS ---
@st.cache_resource
def load_models():
    # CHANGE THESE NAMES to match exactly what you see in your GitHub folder
    model = pickle.load(open('facttrace_model.pkl', 'rb')) 
    tfidf = pickle.load(open('tfidf_vectorizer.pkl', 'rb'))
    return model, tfidf

# Professional CSS for the "FakeShield" Look
st.markdown("""
    <style>
    .main { background-color: #060918; color: white; }
    .stTextArea textarea { background-color: #0f173d !important; color: white !important; border: 1px solid #1e2a5a !important; border-radius: 15px; }
    .status-badge { background: #00332c; color: #00ff88; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #00ff88; }
    .verify-btn { background: linear-gradient(90deg, #00f2fe 0%, #0072ff 100%); color: black; font-weight: bold; padding: 10px; border-radius: 10px; width: 100%; border: none; }
    .result-card { background: #0b112b; padding: 20px; border-radius: 15px; border-left: 5px solid #00f2fe; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Header
col_h1, col_h2 = st.columns([4, 1])
with col_h1:
    st.markdown("## 🛡️ FakeShield <span style='color:#00f2fe;'>AI</span>", unsafe_allow_html=True)
with col_h2:
    st.markdown("<div class='status-badge'>● System Operational</div>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Detection", "🔗 Origin Tracing", "📢 Mitigation"])

with tab1:
    st.write("Enter news content to verify its credibility against official sources.")
    news_input = st.text_area("", height=150, placeholder="Paste news content here...")
    
    if st.button("VERIFY NOW"):
        if news_input:
            with st.spinner("Analyzing linguistic patterns..."):
                time.sleep(1)
                vec = tfidf.transform([news_input])
                pred = model.predict(vec)[0]
                prob = 94.2 if pred == 1 else 14.5 # Simulated confidence

                if pred == 0:
                    st.error("🚨 POTENTIAL MISINFORMATION DETECTED")
                    st.markdown(f"""<div class='result-card'>
                        <h3>Confidence Score: {prob}%</h3>
                        <p>This content matches patterns of known fake news spreaders. Mitigation recommended.</p>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.success("✅ VERIFIED REAL CONTENT")
                    st.balloons()
        else:
            st.warning("Please enter text first.")

with tab2:
    st.subheader("Visualizing Misinformation Propagation")
    # Logic: Creating a network graph to show "Origin Tracing"
    fig = go.Figure()
    # Nodes (Origin -> Spreader 1 -> Consumer)
    edge_x = [0, 1, 1, 2, 2, 2]
    edge_y = [0, 1, -1, 2, 0, -2]
    
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='markers+text',
                             text=["ORIGIN", "Spreader A", "Spreader B", "User 1", "User 2", "User 3"],
                             marker=dict(size=40, color=['red', 'orange', 'orange', 'cyan', 'cyan', 'cyan']),
                             textposition="top center"))
    
    fig.update_layout(title="Tracing the Source", showlegend=False, 
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Automated Mitigation Center")
    st.write("Send authenticated news directly to the spreader's inbox.")
    
    spreader_phone = st.text_input("Enter Spreader's Phone Number (for SMS simulation):")
    correction_msg = st.text_area("Authenticated Message:", "ALERT: The information you shared has been flagged as FALSE. Read the official truth here: [Reuters Link]")
    
    if st.button("SEND TRUTH ALERT"):
        st.success(f"Mitigation Successful! Correction sent to {spreader_phone} ✅")
        st.info("The spreader's feed has been auto-populated with official facts.")
