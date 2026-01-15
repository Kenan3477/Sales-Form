#!/usr/bin/env python3
"""
ASIS Local Development Server
============================
Run ASIS web interface locally for testing
"""

import os
import sys

# Set environment variables
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = 'True'
os.environ['PORT'] = '5000'

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    try:
        from app import app, socketio
        
        print("🚀 Starting ASIS Development Server...")
        print("🌐 Access ASIS at: http://localhost:5000")
        print("📊 Dashboard at: http://localhost:5000/dashboard")
        print("💡 Press Ctrl+C to stop")
        
        # Run the development server
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
        
    except KeyboardInterrupt:
        print("\n🛑 ASIS Development Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)
