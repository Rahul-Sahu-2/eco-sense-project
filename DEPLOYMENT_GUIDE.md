# 🚀 EcoSense Free Deployment Guide

Since your project has a **React Frontend**, a **FastAPI Backend**, and **Large AI Models**, the best way to deploy it for free is using a combination of **Vercel** and **Render**.

---

## 🏗 Deployment Strategy

| Component | Platform | Why? |
|-----------|----------|------|
| **Frontend** | [Vercel](https://vercel.com) | Extremely fast, free, and optimized for React/Vite. |
| **Backend** | [Render](https://render.com) | Best free tier for Python/FastAPI. |
| **AI Models** | GitHub LFS | These files are too big for standard Git. Render will download them during build. |

---

## 🛠 Step 1: Prep the Frontend
Before deploying the frontend, you must tell it where your **Live Backend** is.

1.  Create a file called `.env.production` in your `frontend/` folder.
2.  Add your future backend URL (e.g., `https://eco-sense-api.onrender.com`).
3.  Update `api.js` to use `import.meta.env.VITE_API_URL` instead of `localhost`.

---

## 🛠 Step 2: Deploy Backend on Render
1.  Go to [Render.com](https://render.com) and sign in with GitHub.
2.  Click **New +** -> **Web Service**.
3.  Connect your `eco-sense-project` repository.
4.  **Settings**:
    - **Environment**: `Python`
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5.  **Environment Variables**:
    - Add `GROQ_API_KEY`, `CONTRACT_ADDRESS`, etc., in the Render dashboard (Settings -> Env Vars).

> [!WARNING]
> **Free Tier Limitation**: Render Web Services "sleep" after 15 minutes of inactivity. The first request after a sleep might take 30-50 seconds to start.

---

## 🛠 Step 3: Deploy Frontend on Vercel
1.  Go to [Vercel.com](https://vercel.com) and sign in with GitHub.
2.  Click **Add New** -> **Project**.
3.  Import your `eco-sense-project` repo.
4.  **Settings**:
    - **Root Directory**: Select `frontend`.
    - **Framework Preset**: `Vite`.
    - **Environment Variables**: Add `VITE_API_URL` as your Render backend link.
5.  Click **Deploy**.

---

## ⚠️ Important Deployment Notes

### 1. Large Files (AI Models)
Your `.h5` and `.pt` files are > 500MB. GitHub might block them if not using **Git LFS**. 
Render's free tier has a **512MB RAM limit**. Loading `yolov8m.pt` (which is heavy) might crash the free instance.
**Solution**: Use the smaller `yolov8n.pt` (Nano version) for production to save RAM.

### 2. Persistent Storage
On Render, files like `users.json` are **temporary**. If the server restarts, your data is lost.
**Solution for Hackathon**: For a demo, it's fine. For a real app, use a free cloud database like [Supabase](https://supabase.com) or [MongoDB Atlas].

### 3. CORS
Your `backend/main.py` already allows `allow_origins=["*"]`, so it should work on any deployed URL.

---

## ✅ Final Check
Once both are deployed:
1.  Open your Vercel URL.
2.  Upload an image.
3.  Check if it successfully hits the Render API.

---
*Good luck with your Deployment!* 🚀✨
