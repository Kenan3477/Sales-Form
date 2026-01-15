#!/usr/bin/env python3
"""
🚀 ASIS Railway Minimal Production Application
=============================================

Simplified Railway deployment with essential functionality.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import asyncio
from typing import Dict
from pydantic import BaseModel

# Environment configuration
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL") 
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
JWT_SECRET = os.getenv("JWT_SECRET", "asis-production-secret")
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

# FastAPI app
app = FastAPI(
    title="ASIS Research Platform",
    description="AI-powered research platform",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    return {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "database_configured": bool(DATABASE_URL),
        "redis_configured": bool(REDIS_URL),
        "stripe_configured": bool(STRIPE_SECRET_KEY)
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ASIS Research Platform API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

# Basic user registration model
class UserRegistration(BaseModel):
    email: str
    password: str
    institution: str = None

# Registration endpoint
@app.post("/register")
async def register_user(user: UserRegistration):
    """User registration endpoint"""
    # Basic validation
    if "@" not in user.email:
        raise HTTPException(status_code=400, detail="Invalid email")
    
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password too short")
    
    # Detect academic email
    is_academic = user.email.endswith('.edu')
    discount = 50 if is_academic else 0
    
    return {
        "message": "Registration successful",
        "email": user.email,
        "is_academic": is_academic,
        "discount_percentage": discount,
        "next_steps": "Complete payment setup to access research platform"
    }

# API status
@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    return {
        "api": "online",
        "environment": ENVIRONMENT,
        "services": {
            "database": "configured" if DATABASE_URL else "not_configured",
            "redis": "configured" if REDIS_URL else "not_configured", 
            "stripe": "configured" if STRIPE_SECRET_KEY else "not_configured"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
