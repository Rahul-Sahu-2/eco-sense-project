# 🌌 EcoSense: AI-Powered Waste Management System

EcoSense is a state-of-the-art waste detection and management platform that rewards citizens for environmental contributions using blockchain technology. Featuring the **Aurora Cosmic** theme, it provides a "Satellite Command Center" experience for administrators and a seamless reporting flow for citizens.

---

## ✨ Key Features

### 📡 Satellite Command Center (Admin Dashboard)
- **Aurora Cosmic UI**: A high-tech, glass-morphic interface designed for visual excellence.
- **Dynamic Real-time Map**: Integrated with Light Voyager tiles for precise waste tracking.
- **Smart Analytics**: Real-time statistics on reports, top contributors, and waste distribution.
- **Automated Reporting**: Export comprehensive waste data as CSV for offline analysis.

### 📸 AI Waste Detection
- **Dual-Model Intelligence**: Utilizes CNN and YOLOv8 for accurate waste identification.
- **Instant Verification**: Analyzes citizen uploads to confirm waste presence and type (Recyclable, Hazardous, etc.).
- **Confidence Scoring**: Provides transparency with percentage-based accuracy bars.

### 🦊 Web3 & Blockchain Integration
- **MetaMask Connectivity**: Seamlessly connect Polygon/Ethereum wallets.
- **Automated Rewards**: Earn tokens automatically upon verified waste reports.
- **Persistent Sessions**: Remembers your wallet address for a hassle-free experience.

### 🔐 Secure Authentication
- **Glass-morphic Auth**: Premium Sign-in/Sign-up experience.
- **JWT Protection**: Secure API communication with token-based authorization.
- **Cross-Platform Compatibility**: Robust password hashing optimized for Windows and Linux.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- Node.js 18+
- MetaMask Browser Extension

### 2. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start the API server
python -m uvicorn backend.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Direct Launch
Use the included `start_project.bat` file in the root directory for a one-click launch of both services.

---

## 🛠 Tech Stack
- **Frontend**: React, Vite, Leaflet, Axios, CSS3 (Glass-morphism)
- **Backend**: FastAPI, Pydantic, Python-Jose
- **AI/ML**: TensorFlow (CNN), Ultralytics (YOLOv8), OpenCV
- **Web3**: Web3.py, MetaMask API

---

## 🌍 Contribution
This project is dedicated to making our planet cleaner through AI and decentralization. 

**Owner**: [Rahul-Sahu-2](https://github.com/Rahul-Sahu-2)

---
*Created with ❤️ for EcoSense Project*
