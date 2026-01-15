#!/usr/bin/env python3
"""
Railway WSGI Server
Simple script to bypass Railway's auto-detection
"""
import os
from wsgiref.simple_server import make_server
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our WSGI application
from main import application

def run_server():
    """Run the WSGI server"""
    port = int(os.environ.get('PORT', 8000))
    
    print(f"Starting WSGI server on port {port}")
    print("Application: main:application")
    print("Server: Pure Python WSGI")
    
    # Create the server
    server = make_server('0.0.0.0', port, application)
    
    try:
        print(f"Server running at http://0.0.0.0:{port}")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
        server.server_close()

if __name__ == '__main__':
    run_server()
