#!/usr/bin/env python3
"""
ASIS Web Server
"""

import http.server
import socketserver
import os

class AsisWebHandler(http.server.SimpleHTTPRequestHandler):
    """Custom web handler"""
    
    def do_GET(self):
        print(f"[ASIS] Serving: {self.path}")
        return super().do_GET()

def main():
    """Start web server"""
    port = 8080
    os.chdir(os.path.dirname(__file__))
    
    with socketserver.TCPServer(("", port), AsisWebHandler) as httpd:
        print(f"[ASIS] Web server running on port {port}")
        print(f"[ASIS] Visit: http://localhost:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()
