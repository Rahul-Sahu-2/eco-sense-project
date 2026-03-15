import numpy as np
import cv2
import base64
from ultralytics import YOLO
import logging

logger = logging.getLogger(__name__)

from backend.config import YOLO_MODEL_PATH, RECYCLABLE, NON_RECYCLABLE, HAZARDOUS

_model = None


def get_model():
    global _model
    if _model is None:
        _model = YOLO(YOLO_MODEL_PATH)
    return _model


def classify_item(name: str):
    low = name.lower()
    if low in RECYCLABLE:
        return "recyclable"
    if low in NON_RECYCLABLE:
        return "non_recyclable"
    if low in HAZARDOUS:
        return "hazardous"
    return "unknown"


def detect_from_base64(image_b64: str, conf: float = 0.1):
    """Run YOLO detection on a base64-encoded image frame."""
    # Strip data URL prefix if present
    if "," in image_b64:
        image_b64 = image_b64.split(",")[1]
    
    img_bytes = base64.b64decode(image_b64)
    arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if frame is None:
        return {"items": [], "boxes": [], "annotated_image": None}

    model = get_model()
    results = model.predict(frame, conf=conf)

    items = []
    boxes = []
    seen = set()

    logger.info(f"YOLO run: found {len(results)} results blocks")
    for r in results:
        num_boxes = len(r.boxes) if r.boxes is not None else 0
        logger.info(f"  Result block has {num_boxes} boxes at conf {conf}")
        if r.boxes is None:
            continue
        for box in r.boxes:
            x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
            cls = int(box.cls[0])
            label = model.names[cls]
            confidence = float(box.conf[0])
            category = classify_item(label)

            boxes.append({
                "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                "label": label,
                "confidence": round(confidence, 3),
                "category": category,
            })

            if label not in seen:
                seen.add(label)
                items.append({"name": label, "category": category})

            # Draw on frame (Force green as requested by user)
            color = (0, 255, 0) # Bright Green
            thickness = 3
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
            
            # Draw label background for better visibility
            label_text = f"{label} {confidence:.2f}"
            (w, h), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, (x1, y1 - 25), (x1 + w, y1), color, -1)
            cv2.putText(frame, label_text, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # Encode annotated frame back to base64
    _, buf = cv2.imencode(".jpg", frame)
    annotated_b64 = base64.b64encode(buf).decode("utf-8")

    return {
        "items": items,
        "boxes": boxes,
        "annotated_image": annotated_b64,
    }
