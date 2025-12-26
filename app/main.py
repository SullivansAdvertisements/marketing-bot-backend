from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.research.router import router as research_router
from app.strategy.router import router as strategy_router
from app.creative.router import router as creative_router
from app.campaigns.router import router as campaigns_router

app = FastAPI(title="Real Data Marketing Bot")

app.include_router(auth_router, prefix="/auth")
app.include_router(research_router, prefix="/research")
app.include_router(strategy_router, prefix="/strategy")
app.include_router(creative_router, prefix="/creative")
app.include_router(campaigns_router, prefix="/campaigns")