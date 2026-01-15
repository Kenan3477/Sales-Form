#!/usr/bin/env python3
import subprocess
import sys
import os

print("ASIS Railway Startup Script")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print("Environment variables:")
for key in ['PORT', 'DATABASE_URL', 'REDIS_URL']:
    print(f"  {key}: {'SET' if os.getenv(key) else 'NOT SET'}")

print("\nStarting ASIS Application on port 8000...")
try:
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "app_ultra_minimal:app",
        "--host", "0.0.0.0",
        "--port", "8000"
    ])
except Exception as e:
    print(f"Error starting application: {e}")
    sys.exit(1)
