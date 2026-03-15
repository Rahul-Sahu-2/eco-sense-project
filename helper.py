# helper.py

from ultralytics import YOLO
import cv2
import streamlit as st
import os
import time
import settings

# --------------------------------------
# Load YOLO Waste Detection Model
# --------------------------------------
@st.cache_resource
def load_waste_model():
    """
    Load the trained YOLO waste detection model
    """
    model_path = settings.MODEL_PATH
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")
    model = YOLO(model_path)
    return model


# --------------------------------------
# Detect Waste Objects
# --------------------------------------
def detect_waste(model, image_path):
    """
    Run YOLO detection on the given image
    """
    results = model(image_path)
    return results


# --------------------------------------
# Draw Bounding Boxes on Image
# --------------------------------------
def draw_boxes(model, image, results):
    """
    Draw bounding boxes around detected waste
    """
    detected_classes = []

    for r in results:
        boxes = getattr(r, "boxes", None)
        if boxes is not None:
            for box in boxes:
                # bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                label = model.names[cls]
                detected_classes.append(label)
                # draw rectangle
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # draw label
                cv2.putText(image, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    return image, detected_classes


# --------------------------------------
# Check Waste Category
# --------------------------------------
def check_category(detected_classes):
    """
    Returns dict with recyclable, non_recyclable, hazardous items
    """
    recyclable = []
    non_recyclable = []
    hazardous = []

    for waste in detected_classes:
        if waste in settings.RECYCLABLE:
            recyclable.append(waste)
        elif waste in settings.NON_RECYCLABLE:
            non_recyclable.append(waste)
        elif waste in settings.HAZARDOUS:
            hazardous.append(waste)

    return {
        "recyclable": recyclable,
        "non_recyclable": non_recyclable,
        "hazardous": hazardous
    }


# --------------------------------------
# Save Screenshot of Detection
# --------------------------------------
def save_screenshot(image):
    """
    Save detection screenshot
    """
    folder = getattr(settings, "SCREENSHOT_FOLDER", "screenshots")
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = f"{folder}/detect_{int(time.time())}.jpg"
    cv2.imwrite(filename, image)
    return filename


# --------------------------------------
# Play Webcam for Live Detection
# --------------------------------------
def play_webcam(model):
    """
    Open webcam, detect waste in real-time, show results in Streamlit
    """
    st_frame = st.empty()
    cap = cv2.VideoCapture(getattr(settings, "WEBCAM_PATH", 0))

    # Initialize session_state
    if "stop_webcam" not in st.session_state:
        st.session_state["stop_webcam"] = False
    if "unique_classes" not in st.session_state:
        st.session_state["unique_classes"] = set()
    if "last_detected_items" not in st.session_state:
        st.session_state["last_detected_items"] = []

    stop_button = st.button("Stop Webcam")
    if stop_button:
        st.session_state["stop_webcam"] = True

    while cap.isOpened() and not st.session_state["stop_webcam"]:
        success, frame = cap.read()
        if not success:
            continue

        results = model.predict(frame, conf=0.5)
        detected_classes = []

        for r in results:
            boxes = getattr(r, "boxes", None)
            if boxes is not None:
                for box in boxes:
                    cls = int(box.cls[0])
                    label = model.names[cls]
                    detected_classes.append(label)

        # Update session state only if new classes detected
        new_classes = set(detected_classes)
        if new_classes != st.session_state["unique_classes"]:
            st.session_state["unique_classes"] = new_classes
            st.session_state["last_detected_items"] = list(new_classes)

        # Draw boxes
        display_frame, _ = draw_boxes(model, frame.copy(), results)
        st_frame.image(display_frame, channels="BGR")

    cap.release()