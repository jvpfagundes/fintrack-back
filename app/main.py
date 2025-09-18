from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware




app = FastAPI(
    title="Chronos Backend",
    description="Backend API for Chronos",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://fintrack-front.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")




@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "chronos-backend"}



