# blockchain_page.py

import streamlit as st
from blockchain_reward import reward_user
from web3 import Web3
from dotenv import load_dotenv
import os
import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

load_dotenv()
DEFAULT_WALLET = os.getenv("WALLET_ADDRESS")

@st.cache_resource(show_spinner=False)
def load_cnn_model():
    return load_model("models/waste_model.h5")

def check_waste_cnn(image):
    img = cv2.resize(image, (128, 128)) / 255.0
    prediction = load_cnn_model().predict(np.reshape(img, (1, 128, 128, 3)))
    return (int(np.argmax(prediction)) == 0), float(prediction[0][0]) * 100, float(prediction[0][1]) * 100

def calculate_tokens(waste_confidence):
    return 5 if waste_confidence >= 80 else 3 if waste_confidence >= 60 else 1 if waste_confidence >= 40 else 0

def res_card(kind, title, body):
    st.markdown(f'<div class="res-card {kind}"><div class="res-title">{title}</div><hr class="res-divider"/>{body}</div>', unsafe_allow_html=True)

def conf_bar(label, value, bar_class):
    return (f'<div class="conf-row"><span class="conf-label">{label}</span><span class="conf-value">{value:.1f}%</span></div>'
            f'<div class="conf-bar-bg"><div class="conf-bar-fill {bar_class}" style="width:{value:.1f}%"></div></div>')

def show():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

    .bc-header{text-align:center;padding:2rem 0}
    .bc-header-badge{display:inline-block;font-size:.72rem;font-weight:600;text-transform:uppercase;letter-spacing:2px;color:#00ff88;background:rgba(0,255,136,0.08);border:1px solid rgba(0,255,136,0.2);padding:.3rem 1rem;border-radius:99px;margin-bottom:1rem}
    .bc-header h1{font-family:'Outfit',sans-serif!important;font-size:2.4rem!important;font-weight:800!important;color:#e2e8f0!important;margin:0 0 .6rem!important;letter-spacing:-.5px!important}
    .bc-header p{font-size:.95rem!important;color:#64748b!important;margin:0!important}

    .how-it-works{display:flex;align-items:center;justify-content:center;gap:6px;margin-bottom:2rem;flex-wrap:wrap}
    .hiw-step{display:flex;align-items:center;gap:8px;background:#0c150c;border:1px solid rgba(0,255,136,0.1);border-radius:12px;padding:.6rem 1rem;font-size:.8rem;color:#94a3b8;font-family:'Outfit',sans-serif}
    .hiw-num{width:22px;height:22px;background:rgba(0,255,136,0.1);border:1px solid rgba(0,255,136,0.25);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.68rem;font-weight:700;color:#00ff88;flex-shrink:0}
    .hiw-arrow{color:#2d3748;font-size:1rem}

    .token-stats{display:flex;gap:12px;margin-bottom:2rem}
    .ts-card{flex:1;background:#0c150c;border:1px solid rgba(0,255,136,0.1);border-radius:14px;padding:1rem;text-align:center;transition:border-color .2s,transform .2s}
    .ts-card:hover{border-color:rgba(0,255,136,0.3);transform:translateY(-2px)}
    .ts-icon{font-size:1.3rem;margin-bottom:.3rem}
    .ts-val{font-size:1.3rem;font-weight:800;color:#00ff88;font-family:'Outfit',sans-serif;line-height:1.2}
    .ts-lbl{font-size:.68rem;color:#475569;text-transform:uppercase;letter-spacing:1px;margin-top:4px}

    .section-label{font-family:'Outfit',sans-serif;font-size:.72rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:#475569;margin-bottom:.5rem;display:block}

    .stTextInput>div>div>input{background:#080f08!important;border:1px solid rgba(0,255,136,0.15)!important;border-radius:12px!important;color:#e2e8f0!important;font-family:'DM Mono',monospace!important;font-size:.85rem!important;padding:.75rem 1rem!important;transition:border-color .2s,box-shadow .2s!important}
    .stTextInput>div>div>input:focus{border-color:#00ff88!important;box-shadow:0 0 0 3px rgba(0,255,136,0.1)!important}

    [data-testid="stFileUploader"]>div{background:#080f08!important;border:1.5px dashed rgba(0,255,136,0.2)!important;border-radius:16px!important;transition:all .2s!important}
    [data-testid="stFileUploader"]>div:hover{border-color:rgba(0,255,136,0.45)!important;background:rgba(0,255,136,0.02)!important}

    .preview-wrap{background:#080f08;border:1px solid rgba(0,255,136,0.1);border-radius:16px;overflow:hidden}
    .preview-header{padding:.75rem 1rem;border-bottom:1px solid rgba(255,255,255,0.05);display:flex;align-items:center;justify-content:space-between}
    .preview-title{font-size:.7rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:#475569;font-family:'Outfit',sans-serif}
    .preview-ready{font-size:.65rem;color:#00ff88;background:rgba(0,255,136,0.1);border:1px solid rgba(0,255,136,0.2);padding:.15rem .55rem;border-radius:99px}
    .file-info{display:flex;align-items:center;gap:8px;margin-top:.7rem;padding:.55rem .8rem;background:rgba(255,255,255,0.03);border-radius:8px;border:1px solid rgba(255,255,255,0.05)}
    .file-name{font-family:'DM Mono',monospace;font-size:.76rem;color:#94a3b8;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}

    .empty-preview{background:#080f08;border:1.5px dashed rgba(255,255,255,0.05);border-radius:16px;padding:3.5rem 1rem;text-align:center;color:#334155;font-family:'Outfit',sans-serif;font-size:.83rem}

    .wallet-warn{display:flex;align-items:flex-start;gap:10px;background:rgba(146,64,14,0.12);border:1px solid rgba(146,64,14,0.35);border-radius:12px;padding:.9rem 1.1rem;margin-top:.5rem}
    .wallet-warn-text{font-size:.84rem;color:#fcd34d;font-family:'Outfit',sans-serif;line-height:1.5}

    .stButton>button{font-family:'Outfit',sans-serif!important;font-weight:700!important;font-size:1rem!important;background:transparent!important;color:#00ff88!important;border:1px solid #00ff88!important;border-radius:10px!important;padding:.8rem 2rem!important;transition:all .25s ease!important;letter-spacing:2px!important;text-transform:uppercase!important;box-shadow:0 0 15px rgba(0,255,136,0.1)!important}
    .stButton>button:hover{background:rgba(0,255,136,0.08)!important;transform:translateY(-2px)!important;box-shadow:0 0 25px rgba(0,255,136,0.25)!important;color:#00ff88!important}

    .res-card{border-radius:16px;padding:1.5rem 1.8rem;margin-top:1.2rem;animation:fadeSlideIn .35s ease forwards;font-family:'Outfit',sans-serif}
    .res-card.success{background:linear-gradient(135deg,#052e16,#064e24);border:1px solid #166534}
    .res-card.error  {background:linear-gradient(135deg,#2d0a0a,#1f0606);border:1px solid #991b1b}
    .res-card.warning{background:linear-gradient(135deg,#2d1f04,#1f1506);border:1px solid #92400e}
    .res-title{font-size:1.1rem;font-weight:700;margin-bottom:1rem}
    .res-card.success .res-title{color:#86efac}
    .res-card.error   .res-title{color:#fca5a5}
    .res-card.warning .res-title{color:#fcd34d}
    .res-divider{border:none;border-top:1px solid rgba(255,255,255,0.07);margin:1rem 0}

    .conf-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:.4rem}
    .conf-label{font-size:.82rem;color:#64748b}
    .conf-value{font-size:.82rem;font-weight:600;color:#cbd5e1}
    .conf-bar-bg{background:rgba(255,255,255,0.05);border-radius:99px;height:6px;margin-bottom:1rem;overflow:hidden}
    .conf-bar-fill{height:100%;border-radius:99px}
    .conf-bar-fill.waste    {background:linear-gradient(90deg,#16a34a,#4ade80);box-shadow:0 0 8px rgba(74,222,128,0.3)}
    .conf-bar-fill.non-waste{background:linear-gradient(90deg,#dc2626,#f87171)}

    .token-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(0,255,136,0.1);border:1px solid rgba(0,255,136,0.3);border-radius:99px;padding:.5rem 1.2rem;font-size:.92rem;font-weight:700;color:#00ff88;margin-top:.8rem}
    .tx-box{background:rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:.9rem 1rem;font-family:'DM Mono',monospace;font-size:.75rem;color:#5eead4;word-break:break-all;margin-top:.8rem;line-height:1.6}
    .tip-text{font-size:.82rem;color:#475569;line-height:1.7;margin-top:.5rem}

    @keyframes fadeSlideIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
    </style>""", unsafe_allow_html=True)

    # ── Header ──
    st.markdown("""
    <div class="bc-header">
        <div class="bc-header-badge">⛓ Polygon Blockchain</div>
        <h1>Blockchain Waste Reward</h1>
        <p>Upload a waste image · AI verifies · Earn tokens instantly</p>
    </div>
    <div class="how-it-works">
        <div class="hiw-step"><div class="hiw-num">1</div> Enter Wallet</div><div class="hiw-arrow">→</div>
        <div class="hiw-step"><div class="hiw-num">2</div> Upload Image</div><div class="hiw-arrow">→</div>
        <div class="hiw-step"><div class="hiw-num">3</div> AI Verifies</div><div class="hiw-arrow">→</div>
        <div class="hiw-step"><div class="hiw-num">4</div> 🎁 Earn Tokens</div>
    </div>
    <div class="token-stats">
        <div class="ts-card"><div class="ts-icon">🎯</div><div class="ts-val">40%+</div><div class="ts-lbl">Min Confidence</div></div>
        <div class="ts-card"><div class="ts-icon">🥉</div><div class="ts-val">1 Token</div><div class="ts-lbl">40–59%</div></div>
        <div class="ts-card"><div class="ts-icon">🥈</div><div class="ts-val">3 Tokens</div><div class="ts-lbl">60–79%</div></div>
        <div class="ts-card"><div class="ts-icon">🥇</div><div class="ts-val">5 Tokens</div><div class="ts-lbl">80%+</div></div>
    </div>""", unsafe_allow_html=True)

    # ── Two Column Layout ──
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<span class="section-label">💳 Wallet Address</span>', unsafe_allow_html=True)
        wallet = st.text_input("wallet", value=DEFAULT_WALLET, placeholder="0x...", label_visibility="collapsed")

        if wallet and not Web3.is_address(wallet):
            st.markdown('<div class="wallet-warn"><div>⚠️</div><div class="wallet-warn-text"><b>Invalid Wallet Address</b><br>Enter a valid Ethereum/Polygon address starting with <code>0x</code></div></div>', unsafe_allow_html=True)
            return

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<span class="section-label">🖼️ Upload Waste Image</span>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("upload", type=["png","jpg","jpeg"], label_visibility="collapsed")

    with col_right:
        if uploaded_file:
            st.markdown('<div class="preview-wrap"><div class="preview-header"><div class="preview-title">📸 Image Preview</div><div class="preview-ready">✓ Ready</div></div></div>', unsafe_allow_html=True)
            st.image(Image.open(uploaded_file).convert("RGB"), use_container_width=True)
            st.markdown(f'<div class="file-info"><span>📄</span><span class="file-name">{uploaded_file.name}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-preview"><div style="font-size:2.5rem;margin-bottom:.7rem">🖼️</div><div>Image preview will appear here</div><div style="font-size:.75rem;margin-top:.3rem;color:#1e293b">PNG, JPG, JPEG supported</div></div>', unsafe_allow_html=True)

    if not uploaded_file:
        return

    st.markdown("<br>", unsafe_allow_html=True)
    if not st.button("🔍  Verify & Claim Tokens", use_container_width=True):
        return

    if not wallet:
        res_card("error", "❌ Wallet Address Required", '<div class="tip-text">Please enter your wallet address before verifying.</div>')
        return

    img_array = np.array(Image.open(uploaded_file).convert("RGB"))
    with st.spinner("🧠 AI analyzing image..."):
        is_waste, waste_conf, non_waste_conf = check_waste_cnn(img_array)
        tokens = calculate_tokens(waste_conf) if is_waste else 0

    if not is_waste:
        res_card("error", "🚫 Non-Waste Image Detected",
            conf_bar("Waste Probability", waste_conf, "waste") +
            conf_bar("Non-Waste Probability", non_waste_conf, "non-waste") +
            '<div class="tip-text">❌ <b>No reward issued.</b> Only waste images qualify.<br>Try plastic bottles, paper, metal cans, or other waste items.</div>')
        return

    if tokens == 0:
        res_card("warning", "⚠️ Low Confidence — No Reward",
            conf_bar("Waste Confidence", waste_conf, "waste") +
            '<div class="tip-text">Minimum <b>40% confidence</b> required. Try a clearer image.</div>')
        return

    res_card("success", "✅ Waste Verified Successfully!",
        conf_bar("Waste Confidence", waste_conf, "waste") +
        f'<div class="token-badge">🎁 &nbsp;{tokens} Token{"s" if tokens > 1 else ""} Eligible</div>')

    with st.spinner("⛓ Processing blockchain transaction..."):
        tx = reward_user(wallet, tokens)

    if tx.startswith("0x"):
        res_card("success", "🎉 Tokens Sent Successfully!",
            f'<span class="conf-label">Transaction Hash</span><div class="tx-box">{tx}</div>')
    else:
        res_card("error", "❌ Transaction Failed", f'<div class="tip-text">{tx}</div>')