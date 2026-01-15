#!/usr/bin/env python3
"""
ASIS Railway Ultra-Minimal App - Guaranteed to work
"""

from fastapi import FastAPI
import os
import uvicorn

# Simple FastAPI app
app = FastAPI(title="ASIS Research Platform")

@app.get("/")
def read_root():
    return {"message": "ASIS Research Platform", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/register")
def register(data: dict):
    email = data.get("email", "")
    return {
        "message": "Registration successful",
        "email": email,
        "is_academic": email.endswith('.edu'),
        "discount": 50 if email.endswith('.edu') else 0
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
