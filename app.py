# app.py (Updated)

from pathlib import Path
import os, cv2, time
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import helper, settings, blockchain_page
import citizen_page
import admin_page

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="EcoSense — AI Waste Detection", page_icon="♻️", layout="wide")

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-box">♻</div>
        <div><div class="logo-text">EcoSense</div><div class="logo-sub">WASTE · AI · BLOCKCHAIN</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<p class="sidebar-label">// Navigation</p>', unsafe_allow_html=True)

    page = st.selectbox("", [
        "🤖 AI Detection",
        "📍 Report Waste & Earn",
        "📊 Admin Panel"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<p class="sidebar-label">// System Stats</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-stats">
        <div class="stat-item"><span class="stat-icon">🎯</span><div><div class="stat-val">92%</div><div class="stat-lbl">Accuracy</div></div></div>
        <div class="stat-item"><span class="stat-icon">🗂️</span><div><div class="stat-val">15+</div><div class="stat-lbl">Waste Classes</div></div></div>
        <div class="stat-item"><span class="stat-icon">⚡</span><div><div class="stat-val">Live</div><div class="stat-lbl">Detection</div></div></div>
        <div class="stat-item"><span class="stat-icon">⛓</span><div><div class="stat-val">Polygon</div><div class="stat-lbl">Blockchain</div></div></div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<p class="sidebar-footer">// YOLOv8 + GROQ + POLYGON</p>', unsafe_allow_html=True)

if "groq_client" not in st.session_state:
    st.session_state["groq_client"] = client

# ── AI FUNCTIONS ──
def ask_groq(system_msg, user_msg):
    try:
        return client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"system","content":system_msg},{"role":"user","content":user_msg}]
        ).choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def get_short_tip(items):
    return ask_groq(
        "You are an Environmental Waste Management Expert. Give a short 2-3 sentence professional tip about proper disposal or recycling.",
        f"Detected waste: {', '.join(i.replace('_',' ') for i in items)}. Quick recommendation?"
    )

def get_deep_explanation(items):
    return ask_groq(
        "You are a professional Waste Management Expert. Explain in structured format: 1) Category 2) Why 3) Disposal steps 4) Environmental impact 5) Safety 6) Sustainability tips",
        f"Detected: {', '.join(i.replace('_',' ') for i in items)}. Explain in detail."
    )

# ══════════════════════════════════════════
# PAGE: CITIZEN REPORT + BLOCKCHAIN REWARD
# ══════════════════════════════════════════
if "Report Waste" in page:
    citizen_page.show()

# ══════════════════════════════════════════
# PAGE: ADMIN PANEL
# ══════════════════════════════════════════
elif "Admin Panel" in page:
    admin_page.show()

# ══════════════════════════════════════════
# PAGE: AI DETECTION
# ══════════════════════════════════════════
elif "AI Detection" in page:

    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <div class="hero-eyebrow"><span class="dot"></span> AI-POWERED ENVIRONMENTAL TECH</div>
            <h1 class="hero-title">Intelligent Waste<br><span class="hero-accent">Segregation System</span></h1>
            <p class="hero-subtitle">Real-time waste detection using YOLOv8 computer vision. Classify, segregate, and get AI-powered recycling guidance — instantly.</p>
        </div>
    </div>
    <div style="display:flex;gap:12px;width:100%;margin:1.5rem 0 1rem;">
        <div style="flex:1;position:relative;height:200px;border-radius:14px;overflow:hidden;border:1px solid rgba(0,255,136,0.15);cursor:pointer;">
            <img src="https://images.unsplash.com/photo-1535378917042-10a22c95931a?w=600&q=80" style="width:100%;height:100%;object-fit:cover;filter:brightness(.65) saturate(.8);display:block;"/>
            <div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,.9));padding:.6rem .9rem;font-family:monospace;font-size:.65rem;letter-spacing:2px;color:#00ff88;">// AI DETECTION</div>
        </div>
        <div style="flex:1;position:relative;height:200px;border-radius:14px;overflow:hidden;border:1px solid rgba(0,255,136,0.15);cursor:pointer;">
            <img src="https://images.unsplash.com/photo-1604187351574-c75ca79f5807?w=600&q=80" style="width:100%;height:100%;object-fit:cover;filter:brightness(.65) saturate(.8);display:block;"/>
            <div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,.9));padding:.6rem .9rem;font-family:monospace;font-size:.65rem;letter-spacing:2px;color:#00ff88;">// SEGREGATION</div>
        </div>
        <div style="flex:1;position:relative;height:200px;border-radius:14px;overflow:hidden;border:1px solid rgba(0,255,136,0.15);cursor:pointer;">
            <img src="https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?w=600&q=80" style="width:100%;height:100%;object-fit:cover;filter:brightness(.65) saturate(.8);display:block;"/>
            <div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,.9));padding:.6rem .9rem;font-family:monospace;font-size:.65rem;letter-spacing:2px;color:#00ff88;">// ECO IMPACT</div>
        </div>
    </div>
    <div class="feature-pills">
        <span class="pill green">⚡ Live Webcam Detection</span>
        <span class="pill teal">🤖 AI-Powered Tips</span>
        <span class="pill amber">♻️ Smart Categorization</span>
        <span class="pill red">☣️ Hazard Detection</span>
        <span class="pill green">🎯 92% Accuracy</span>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📷  Waste Detection", "🤖  AI Chatbot"])

    # ── TAB 1: DETECTION ──
    with tab1:
        try:
            model = helper.load_waste_model()
        except Exception as ex:
            st.error(f"Model load failed: {ex}")

        if st.session_state.get("show_result") and st.session_state.get("last_detected_items"):
            items      = st.session_state["last_detected_items"]
            screenshot = st.session_state.get("last_screenshot")
            recyclable     = [i for i in items if i.lower() in settings.RECYCLABLE]
            non_recyclable = [i for i in items if i.lower() in settings.NON_RECYCLABLE]
            hazardous      = [i for i in items if i.lower() in settings.HAZARDOUS]

            for col, icon, val, lbl, cls in zip(
                st.columns(4),
                ["🔍","♻️","⛔","☣️"],
                [len(items), len(recyclable), len(non_recyclable), len(hazardous)],
                ["Items Detected","Recyclable","Non-Recyclable","Hazardous"],
                ["","green","blue","red"]
            ):
                with col:
                    st.markdown(f'<div class="metric-card {cls}"><div class="metric-icon">{icon}</div><div class="metric-val">{val}</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1.1, 1, 1])

            with col1:
                st.markdown('<p class="col-label">// Detected Frame</p>', unsafe_allow_html=True)
                if screenshot is not None and screenshot.size > 0:
                    st.image(screenshot, channels="BGR", use_container_width=True)

            with col2:
                st.markdown('<p class="col-label">// Classification</p>', unsafe_allow_html=True)
                if not any([recyclable, non_recyclable, hazardous]):
                    st.warning("No categorized items detected.")
                if recyclable:
                    st.markdown("<div class='stRecyclable'><b>✅ Recyclable</b><br>• " + "<br>• ".join(recyclable) + "</div>", unsafe_allow_html=True)
                if non_recyclable:
                    st.markdown("<div class='stNonRecyclable'><b>⛔ Non-Recyclable</b><br>• " + "<br>• ".join(non_recyclable) + "</div>", unsafe_allow_html=True)
                if hazardous:
                    st.markdown("<div class='stHazardous'><b>☣️ Hazardous</b><br>• " + "<br>• ".join(hazardous) + "</div>", unsafe_allow_html=True)

            with col3:
                st.markdown('<p class="col-label">// AI Quick Tip</p>', unsafe_allow_html=True)
                with st.spinner("Generating..."):
                    tip = get_short_tip(items)
                st.markdown(f'<div class="tip-card"><div class="tip-icon">🌿</div><p>{tip}</p><div class="tip-footer">// See Chatbot tab for full analysis</div></div>', unsafe_allow_html=True)

            st.session_state["detected_for_chatbot"] = items
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄  Detect Again", use_container_width=True):
                st.session_state.update({"show_result":False,"last_detected_items":[],"last_screenshot":None,"detected_for_chatbot":[],"chat_history":[]})
                st.rerun()

        else:
            st.markdown("""
            <div class="detection-panel">
                <div style="display:flex;gap:12px;width:100%;margin-bottom:2rem;">
                    <div style="flex:1;position:relative;height:150px;border-radius:14px;overflow:hidden;border:1px solid rgba(0,255,136,0.15);">
                        <img src="https://images.unsplash.com/photo-1567177662154-dfeb4c93b6ae?w=400&q=80" style="width:100%;height:100%;object-fit:cover;filter:brightness(.6) saturate(.8);display:block;"/>
                        <div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,.9));padding:.5rem .8rem;font-family:monospace;font-size:.6rem;letter-spacing:2px;color:#00ff88;">// WASTE INPUT</div>
                    </div>
                    <div style="flex:1;position:relative;height:150px;border-radius:14px;overflow:hidden;border:1px solid rgba(0,255,136,0.15);">
                        <img src="https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400&q=80" style="width:100%;height:100%;object-fit:cover;filter:brightness(.6) saturate(.8);display:block;"/>
                        <div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,.9));padding:.5rem .8rem;font-family:monospace;font-size:.6rem;letter-spacing:2px;color:#00ff88;">// AI PROCESSING</div>
                    </div>
                    <div style="flex:1;position:relative;height:150px;border-radius:14px;overflow:hidden;border:1px solid rgba(0,255,136,0.15);">
                        <img src="https://images.unsplash.com/photo-1507146153580-69a1fe6d8aa1?w=400&q=80" style="width:100%;height:100%;object-fit:cover;filter:brightness(.6) saturate(.8);display:block;"/>
                        <div style="position:absolute;bottom:0;left:0;right:0;background:linear-gradient(transparent,rgba(0,0,0,.9));padding:.5rem .8rem;font-family:monospace;font-size:.6rem;letter-spacing:2px;color:#00ff88;">// ECO OUTPUT</div>
                    </div>
                </div>
                <div class="steps-row">
                    <div class="step-card"><div class="step-num">01</div><div class="step-txt">Allow webcam access</div></div>
                    <div class="step-arrow">→</div>
                    <div class="step-card"><div class="step-num">02</div><div class="step-txt">Hold waste in front of camera</div></div>
                    <div class="step-arrow">→</div>
                    <div class="step-card"><div class="step-num">03</div><div class="step-txt">AI detects in 5 seconds</div></div>
                    <div class="step-arrow">→</div>
                    <div class="step-card"><div class="step-num">04</div><div class="step-txt">Get recycling tips + tokens</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("▶  START DETECTION", use_container_width=True):
                cap        = cv2.VideoCapture(getattr(settings, "WEBCAM_PATH", 0))
                st_frame   = st.empty()
                status_txt = st.empty()
                detected   = set()
                last_frame = None
                t0         = time.time()

                while time.time() - t0 < 10:
                    ok, frame = cap.read()
                    if not ok: continue
                    elapsed   = time.time() - t0
                    pct       = int((elapsed / 5) * 100)
                    status_txt.markdown(f"""
                    <div class="detect-progress">
                        <div class="dp-top"><span>// SCANNING...</span><span>{max(0, 5-int(elapsed))}s</span></div>
                        <div class="prog-bar-bg"><div class="prog-bar-fill" style="width:{pct}%"></div></div>
                    </div>""", unsafe_allow_html=True)
                    results = model.predict(frame, conf=0.5)
                    for r in results:
                        for box in (r.boxes or []):
                            detected.add(model.names[int(box.cls[0])])
                    last_frame, _ = helper.draw_boxes(model, frame, results)
                    st_frame.image(last_frame, channels="BGR", use_container_width=True)

                cap.release(); st_frame.empty(); status_txt.empty()
                if last_frame is not None:
                    helper.save_screenshot(last_frame)
                    st.session_state.update({"last_screenshot":last_frame,"last_detected_items":list(detected),"show_result":True})
                st.rerun()

    # ── TAB 2: CHATBOT ──
    with tab2:
        st.markdown("""
        <div class="chatbot-header">
            <div class="chatbot-avatar">🤖</div>
            <div>
                <div class="chatbot-title">Waste Management AI Assistant</div>
                <div class="chatbot-status"><span class="status-dot"></span> ONLINE — READY</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.get("detected_for_chatbot"):
            items = st.session_state["detected_for_chatbot"]
            st.markdown(f'<div class="detected-banner">// Auto-analyzing: <b>{", ".join(items)}</b></div>', unsafe_allow_html=True)
            with st.spinner("Generating analysis..."):
                deep_tip = get_deep_explanation(items)
            st.markdown("### 📋 Detailed Analysis")
            st.write(deep_tip)
            st.markdown("---")
            st.session_state["detected_for_chatbot"] = []

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for msg in st.session_state.chat_history:
            st.chat_message(msg["role"]).write(msg["text"])

        if user_input := st.chat_input("Ask about waste disposal, recycling, hazardous materials..."):
            st.chat_message("user").write(user_input)
            st.session_state.chat_history.append({"role":"user","text":user_input})
            with st.spinner("Thinking..."):
                ans = ask_groq(
                    "You are a professional Waste Management Assistant. Provide detailed, clear, educational explanations about waste disposal, recycling, hazardous waste, and environmental impact.",
                    user_input
                )
            st.chat_message("assistant").write(ans)
            st.session_state.chat_history.append({"role":"assistant","text":ans})

# ══════════════════════════════════════════
# PAGE: BLOCKCHAIN REWARD (standalone)
# ══════════════════════════════════════════
else:
    blockchain_page.show()