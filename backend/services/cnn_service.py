import numpy as np
import cv2
import logging

logger = logging.getLogger(__name__)

_model = None
_model_failed = False


def _get_model():
    global _model, _model_failed
    if _model_failed:
        return None
    if _model is not None:
        return _model
    try:
        from backend.config import CNN_MODEL_PATH
        from tensorflow.keras.models import load_model as keras_load
        _model = keras_load(CNN_MODEL_PATH)
        logger.info("CNN model loaded successfully")
        return _model
    except Exception as e:
        logger.warning(f"CNN model load failed (using heuristic fallback): {e}")
        _model_failed = True
        return None


def detect_waste_type(image_array: np.ndarray) -> str:
    """Heuristic waste-type classification based on HSV color analysis."""
    hsv = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)
    avg_hue = float(np.mean(hsv[:, :, 0]))
    avg_sat = float(np.mean(hsv[:, :, 1]))
    avg_val = float(np.mean(hsv[:, :, 2]))

    if avg_sat < 30:
        return "Paper / Cardboard"
    elif avg_hue < 15 or avg_hue > 160:
        return "Plastic"
    elif 15 < avg_hue < 35:
        return "Organic"
    elif 90 < avg_hue < 130:
        return "Metal / Glass"
    else:
        return "Mixed Waste"


def _heuristic_waste_score(image_array: np.ndarray) -> float:
    """Estimate waste likelihood using image features when CNN unavailable."""
    hsv = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)
    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

    # Texture complexity (waste tends to be more textured)
    edges = cv2.Canny(gray, 50, 150)
    edge_ratio = np.count_nonzero(edges) / edges.size

    # Color variance (waste images usually have more color variation)
    sat_std = float(np.std(hsv[:, :, 1]))
    val_std = float(np.std(hsv[:, :, 2]))

    # Combine features into a score (0-100)
    # Be more generous with the score to avoid "non-waste" false negatives
    score = min(100, max(30, (edge_ratio * 400) + (sat_std * 0.5) + (val_std * 0.4)))
    return round(score, 1)


def analyze_waste_image(image_array: np.ndarray) -> dict:
    """Run CNN model or fallback heuristic to determine waste vs non-waste."""
    model = _get_model()

    if model is not None:
        img = cv2.resize(image_array, (128, 128)) / 255.0
        img_input = np.reshape(img, (1, 128, 128, 3))
        prediction = model.predict(img_input)
        waste_conf = float(prediction[0][0]) * 100
        non_waste_conf = float(prediction[0][1]) * 100
        is_waste = int(np.argmax(prediction[0])) == 0
    else:
        # Heuristic fallback
        waste_conf = _heuristic_waste_score(image_array)
        non_waste_conf = 100.0 - waste_conf
        is_waste = waste_conf >= 50

    waste_type = detect_waste_type(image_array)

    return {
        "is_waste": is_waste,
        "waste_percent": round(waste_conf, 1),
        "non_waste_percent": round(non_waste_conf, 1),
        "waste_type": waste_type,
    }


def check_waste_cnn(image_array: np.ndarray):
    """Quick waste check returning (is_waste, waste_conf, non_waste_conf)."""
    model = _get_model()

    if model is not None:
        img = cv2.resize(image_array, (128, 128)) / 255.0
        prediction = model.predict(np.reshape(img, (1, 128, 128, 3)))
        return (
            int(np.argmax(prediction[0])) == 0,
            float(prediction[0][0]) * 100,
            float(prediction[0][1]) * 100,
        )
    else:
        # Heuristic fallback
        score = _heuristic_waste_score(image_array)
        return (score >= 50, score, 100.0 - score)
