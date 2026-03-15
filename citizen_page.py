import streamlit as st
import pandas as pd
import os
import numpy as np
import cv2
from datetime import datetime
from streamlit_js_eval import get_geolocation
from blockchain_reward import reward_user
from web3 import Web3
from PIL import Image
from tensorflow.keras.models import load_model

CSV_PATH = "database/reports.csv"
MODEL_PATH = "models/waste_model.h5"
WASTE_THRESHOLD = 70


# ─────────────────────────────
# Load AI Model
# ─────────────────────────────
@st.cache_resource(show_spinner=False)
def load_waste_model():
    return load_model(MODEL_PATH)


# ─────────────────────────────
# Waste Detection
# ─────────────────────────────
def analyze_waste_image(image_array):

    model = load_waste_model()

    img = cv2.resize(image_array, (128, 128)) / 255.0
    img_input = np.reshape(img, (1, 128, 128, 3))

    prediction = model.predict(img_input)

    waste_conf = float(prediction[0][0]) * 100
    non_waste_conf = float(prediction[0][1]) * 100

    is_waste = int(np.argmax(prediction[0])) == 0

    waste_type = detect_waste_type(image_array)

    return {
        "is_waste": is_waste,
        "waste_percent": round(waste_conf, 1),
        "non_waste_percent": round(non_waste_conf, 1),
        "waste_type": waste_type
    }


# ─────────────────────────────
# Waste Type Detection
# ─────────────────────────────
def detect_waste_type(image_array):

    hsv = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)

    avg_hue = np.mean(hsv[:, :, 0])
    avg_sat = np.mean(hsv[:, :, 1])

    if avg_sat < 30:
        return "Paper / Cardboard"

    elif avg_hue < 15 or avg_hue > 160:
        return "Plastic"

    elif 15 < avg_hue < 35:
        return "Organic"

    else:
        return "Mixed"


# ─────────────────────────────
# Waste Level for Map
# ─────────────────────────────
def get_waste_level(percent):

    if percent >= 80:
        return "HIGH"

    elif percent >= 50:
        return "MEDIUM"

    else:
        return "LOW"


# ─────────────────────────────
# Token Calculation
# ─────────────────────────────
def calculate_tokens(waste_percent):

    if waste_percent >= 90:
        return 5

    elif waste_percent >= 80:
        return 3

    elif waste_percent >= 70:
        return 1

    else:
        return 0


# ─────────────────────────────
# Save Report
# ─────────────────────────────
def save_report(name, waste_type, waste_percent, lat, lon, wallet, tx_hash, tokens):

    os.makedirs("database", exist_ok=True)

    waste_level = get_waste_level(waste_percent)

    new_row = {
        "name": name,
        "waste_type": waste_type,
        "waste_percent": waste_percent,
        "waste_level": waste_level,
        "lat": lat,
        "lon": lon,
        "wallet": wallet,
        "tokens_earned": tokens,
        "tx_hash": tx_hash,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    df.to_csv(CSV_PATH, index=False)


# ─────────────────────────────
# MAIN PAGE
# ─────────────────────────────
def show():

    st.title("📍 Report Waste & Earn Tokens")

    st.write("Upload garbage photo → AI verifies → Earn blockchain tokens")

    # ───────── LOCATION ─────────
    st.subheader("Step 1: Capture Location")

    location = get_geolocation()

    lat, lon = None, None

    if location is None:

        st.warning("Allow location permission")

    else:

        lat = location["coords"]["latitude"]
        lon = location["coords"]["longitude"]

        st.success(f"Location captured: {lat} , {lon}")

    # ───────── IMAGE UPLOAD ─────────
    st.subheader("Step 2: Upload Waste Photo")

    uploaded_photo = st.file_uploader(
        "Upload garbage image",
        type=["jpg", "jpeg", "png"]
    )

    ai_result = None

    if uploaded_photo:

        col1, col2 = st.columns(2)

        with col1:

            st.image(uploaded_photo)

        with col2:

            with st.spinner("AI analyzing..."):

                image = Image.open(uploaded_photo).convert("RGB")

                image_array = np.array(image)

                ai_result = analyze_waste_image(image_array)

                waste_pct = ai_result["waste_percent"]
                non_waste_pct = ai_result["non_waste_percent"]

                waste_type = ai_result["waste_type"]

                is_waste = ai_result["is_waste"]

                st.markdown(f"""
                **Waste Confidence:** {waste_pct}%

                **Non Waste:** {non_waste_pct}%

                **Detected Type:** {waste_type}

                **Verified:** {"Waste Confirmed" if is_waste else "Not Waste"}
                """)

                st.progress(int(waste_pct))

    # ───────── USER FORM ─────────
    st.subheader("Step 3: Submit Report")

    with st.form("report_form"):

        name = st.text_input("Your Name")

        wallet = st.text_input("Polygon Wallet Address")

        submit = st.form_submit_button("Submit Report")

        if submit:

            if not name:
                st.error("Enter name")

            elif lat is None:
                st.error("Location not captured")

            elif uploaded_photo is None:
                st.error("Upload image")

            elif ai_result is None:
                st.error("AI result missing")

            elif not ai_result["is_waste"]:
                st.error("Image is not waste")

            elif ai_result["waste_percent"] < WASTE_THRESHOLD:
                st.error("Waste confidence too low")

            elif not Web3.is_address(wallet):
                st.error("Invalid wallet address")

            else:

                waste_pct = ai_result["waste_percent"]
                waste_type = ai_result["waste_type"]

                tokens = calculate_tokens(waste_pct)

                tx_hash = ""

                if tokens > 0:

                    with st.spinner("Processing blockchain..."):

                        tx_hash = reward_user(wallet, tokens)

                save_report(
                    name,
                    waste_type,
                    waste_pct,
                    lat,
                    lon,
                    wallet,
                    tx_hash,
                    tokens
                )

                st.success("Report submitted!")

                st.write("Tokens earned:", tokens)

                if tx_hash:
                    st.code(tx_hash)