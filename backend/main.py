from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import detection, chatbot, citizen, blockchain, admin, auth

app = FastAPI(
    title="EcoSense API",
    description="AI-powered waste detection and blockchain rewards",
    version="2.0.0",
)

# CORS — allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(detection.router)
app.include_router(chatbot.router)
app.include_router(citizen.router)
app.include_router(blockchain.router)
app.include_router(admin.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {
        "app": "EcoSense API",
        "version": "2.0.0",
        "status": "running",
    }
