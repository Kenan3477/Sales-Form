#!/usr/bin/env python3
import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs

class ASISHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            response = {"message": "ASIS Research Platform", "status": "running"}
        elif parsed_path.path == '/health':
            response = {"status": "healthy"}
        else:
            self.send_response(404)
            self.end_headers()
            return
            
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        if self.path == '/register':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                email = data.get('email', '')
                response = {
                    "message": "Registration successful",
                    "email": email,
                    "is_academic": email.endswith('.edu'),
                    "discount": 50 if email.endswith('.edu') else 0
                }
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            except:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    PORT = 8000
    print(f"Starting ASIS server on port {PORT}")
    with socketserver.TCPServer(("", PORT), ASISHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        httpd.serve_forever()
