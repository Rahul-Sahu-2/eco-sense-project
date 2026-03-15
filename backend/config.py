import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (parent of backend/)
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# ── API Keys ──
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
RPC_URL = os.getenv("RPC_URL", "")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS", "")

# ── Model Paths ──
YOLO_MODEL_PATH = str(ROOT_DIR / "weights" / "best.pt")
CNN_MODEL_PATH = str(ROOT_DIR / "models" / "waste_model.h5")

# ── Data Paths ──
CSV_PATH = str(ROOT_DIR / "database" / "reports.csv")
SCREENSHOT_FOLDER = str(ROOT_DIR / "screenshots")

# ── Waste Categories ──
RECYCLABLE = [
    "cardboard_box", "can", "plastic_bottle_cap",
    "plastic_bottle", "reuseable_paper",
]
NON_RECYCLABLE = [
    "plastic_bag", "scrap_paper", "stick", "plastic_cup",
    "snack_bag", "plastic_box", "straw", "plastic_cup_lid",
    "scrap_plastic", "cardboard_bowl", "plastic_cultery",
]
HAZARDOUS = [
    "battery", "chemical_spray_can", "chemical_plastic_bottle",
    "chemical_plastic_gallon", "light_bulb", "paint_bucket",
]
