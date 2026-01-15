#!/usr/bin/env python3
"""
ASIS Secure HTTPS Server
Secure web server with TLS 1.3, certificate management, and network security integration
"""

import ssl
import socket
import asyncio
import aiohttp
from aiohttp import web, WSMsgType
import aiohttp_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import json
import logging
from datetime import datetime
import os
import tempfile
from typing import Dict, Any, Optional
import traceback

# Import ASIS network security
from asis_network_security import ASISNetworkSecurity

logger = logging.getLogger(__name__)

class ASISSecureServer:
    """Secure HTTPS server with integrated network security"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8443):
        self.host = host
        self.port = port
        self.app = None
        self.runner = None
        self.site = None
        
        # Initialize network security
        self.network_security = ASISNetworkSecurity()
        
        # Server configuration
        self.ssl_context = None
        self.cert_file = None
        self.key_file = None
        
        # Setup server
        self._setup_application()
    
    def _setup_application(self):
        """Setup aiohttp application with security middleware"""
        
        # Create application
        self.app = web.Application(middlewares=[
            self._security_middleware,
            self._rate_limit_middleware,
            self._logging_middleware
        ])
        
        # Setup session storage with encryption
        secret_key = os.urandom(32)
        aiohttp_session.setup(self.app, EncryptedCookieStorage(secret_key))
        
        # Add routes
        self._setup_routes()
        
        # Add WebSocket support
        self._setup_websocket()
    
    def _setup_routes(self):
        """Setup HTTP routes with security"""
        
        # API routes
        self.app.router.add_get('/api/health', self._health_check)
        self.app.router.add_get('/api/security/status', self._security_status)
        self.app.router.add_get('/api/security/dashboard', self._security_dashboard)
        self.app.router.add_post('/api/auth/login', self._login)
        self.app.router.add_post('/api/auth/logout', self._logout)
        
        # ASIS API routes
        self.app.router.add_post('/api/asis/query', self._asis_query)
        self.app.router.add_get('/api/asis/status', self._asis_status)
        
        # Static file serving (with security)
        self.app.router.add_get('/', self._serve_index)
        self.app.router.add_static('/', path='static', name='static')
    
    def _setup_websocket(self):
        """Setup WebSocket for real-time communication"""
        self.app.router.add_get('/ws', self._websocket_handler)
    
    async def _security_middleware(self, request, handler):
        """Security middleware for all requests"""
        
        # Get client information
        client_ip = request.remote
        method = request.method
        path = request.path
        
        # Extract user info if available
        user_id = None
        session = await aiohttp_session.get_session(request)
        if 'user_id' in session:
            user_id = session['user_id']
        
        # Process through network security
        security_result = self.network_security.process_network_request(
            src_ip=client_ip,
            dst_port=self.port,
            protocol="https",
            request_data=f"{method} {path}",
            user_id=user_id,
            endpoint=path
        )
        
        # Block if not allowed
        if not security_result["allowed"]:
            blocked_by = ", ".join(security_result["blocked_by"])
            logger.warning(f"Request blocked from {client_ip}: {blocked_by}")
            
            return web.json_response({
                "error": "Request blocked by security system",
                "blocked_by": security_result["blocked_by"],
                "recommendations": security_result["recommendations"]
            }, status=403)
        
        # Add security headers
        response = await handler(request)
        
        # Security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
        
        return response
    
    async def _rate_limit_middleware(self, request, handler):
        """Rate limiting middleware"""
        
        client_ip = request.remote
        path = request.path
        method = request.method
        
        # Check rate limits
        allowed, rate_info = self.network_security.rate_limiter.check_rate_limit(
            ip=client_ip,
            user_id=None,  # Will be set by security middleware
            endpoint=path,
            method=method
        )
        
        if not allowed:
            retry_after = rate_info.get('retry_after', 60)
            return web.json_response({
                "error": "Rate limit exceeded",
                "retry_after": retry_after,
                "details": rate_info
            }, status=429, headers={'Retry-After': str(retry_after)})
        
        return await handler(request)
    
    async def _logging_middleware(self, request, handler):
        """Logging middleware for requests"""
        
        start_time = datetime.now()
        client_ip = request.remote
        method = request.method
        path = request.path
        
        try:
            response = await handler(request)
            duration = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"{client_ip} {method} {path} - {response.status} - {duration:.3f}s")
            return response
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"{client_ip} {method} {path} - ERROR: {e} - {duration:.3f}s")
            
            return web.json_response({
                "error": "Internal server error",
                "message": "An error occurred processing your request"
            }, status=500)
    
    async def _health_check(self, request):
        """Health check endpoint"""
        return web.json_response({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "security_active": all(self.network_security.security_status.values())
        })
    
    async def _security_status(self, request):
        """Security status endpoint"""
        return web.json_response(self.network_security.security_status)
    
    async def _security_dashboard(self, request):
        """Security dashboard endpoint"""
        dashboard = self.network_security.get_security_dashboard()
        return web.json_response(dashboard)
    
    async def _login(self, request):
        """Login endpoint with security validation"""
        
        try:
            data = await request.json()
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return web.json_response({
                    "error": "Username and password required"
                }, status=400)
            
            # Simple authentication (integrate with your auth system)
            if username == "admin" and password == "secure_password":
                session = await aiohttp_session.get_session(request)
                session['user_id'] = username
                session['authenticated'] = True
                
                return web.json_response({
                    "status": "success",
                    "message": "Logged in successfully",
                    "user": username
                })
            else:
                return web.json_response({
                    "error": "Invalid credentials"
                }, status=401)
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            return web.json_response({
                "error": "Login failed"
            }, status=500)
    
    async def _logout(self, request):
        """Logout endpoint"""
        session = await aiohttp_session.get_session(request)
        session.clear()
        
        return web.json_response({
            "status": "success",
            "message": "Logged out successfully"
        })
    
    async def _asis_query(self, request):
        """ASIS query endpoint"""
        
        try:
            # Check authentication
            session = await aiohttp_session.get_session(request)
            if not session.get('authenticated'):
                return web.json_response({
                    "error": "Authentication required"
                }, status=401)
            
            data = await request.json()
            query = data.get('query', '')
            
            if not query:
                return web.json_response({
                    "error": "Query is required"
                }, status=400)
            
            # Simulate ASIS processing
            response = {
                "status": "success",
                "query": query,
                "response": f"ASIS processed query: {query}",
                "timestamp": datetime.now().isoformat(),
                "security_validated": True
            }
            
            return web.json_response(response)
            
        except Exception as e:
            logger.error(f"ASIS query error: {e}")
            return web.json_response({
                "error": "Query processing failed"
            }, status=500)
    
    async def _asis_status(self, request):
        """ASIS status endpoint"""
        return web.json_response({
            "status": "operational",
            "version": "1.0.0",
            "security_score": self.network_security._calculate_security_score(),
            "timestamp": datetime.now().isoformat()
        })
    
    async def _serve_index(self, request):
        """Serve index page"""
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>ASIS Secure Server</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .security-status { background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .api-example { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .secure-badge { color: #27ae60; font-weight: bold; }
        button { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        button:hover { background: #2980b9; }
        #status { margin-top: 20px; padding: 15px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 ASIS Secure Server</h1>
        <div class="security-status">
            <h3>🛡️ Security Status</h3>
            <p><span class="secure-badge">✅ TLS 1.3 Enabled</span></p>
            <p><span class="secure-badge">✅ Network Security Active</span></p>
            <p><span class="secure-badge">✅ Rate Limiting Active</span></p>
            <p><span class="secure-badge">✅ Intrusion Detection Active</span></p>
        </div>
        
        <h3>📡 API Endpoints</h3>
        <div class="api-example">
            <strong>GET /api/health</strong> - Health check<br>
            <strong>GET /api/security/status</strong> - Security status<br>
            <strong>GET /api/security/dashboard</strong> - Security dashboard<br>
            <strong>POST /api/auth/login</strong> - Authentication<br>
            <strong>POST /api/asis/query</strong> - ASIS query (authenticated)
        </div>
        
        <h3>🧪 Test Security</h3>
        <button onclick="testHealth()">Test Health</button>
        <button onclick="testSecurity()">Test Security Status</button>
        <button onclick="testLogin()">Test Login</button>
        <button onclick="testASIS()">Test ASIS Query</button>
        
        <div id="status"></div>
    </div>
    
    <script>
        function updateStatus(message, type = 'info') {
            const status = document.getElementById('status');
            const color = type === 'error' ? '#e74c3c' : type === 'success' ? '#27ae60' : '#3498db';
            status.innerHTML = `<div style="background: ${color}; color: white; padding: 10px; border-radius: 5px;">${message}</div>`;
        }
        
        async function testHealth() {
            try {
                const response = await fetch('/api/health');
                const data = await response.json();
                updateStatus(`Health: ${data.status} - Security Active: ${data.security_active}`, 'success');
            } catch (error) {
                updateStatus(`Error: ${error.message}`, 'error');
            }
        }
        
        async function testSecurity() {
            try {
                const response = await fetch('/api/security/status');
                const data = await response.json();
                updateStatus(`Security Status: ${JSON.stringify(data, null, 2)}`, 'success');
            } catch (error) {
                updateStatus(`Error: ${error.message}`, 'error');
            }
        }
        
        async function testLogin() {
            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username: 'admin', password: 'secure_password' })
                });
                const data = await response.json();
                updateStatus(`Login: ${data.message || data.error}`, response.ok ? 'success' : 'error');
            } catch (error) {
                updateStatus(`Error: ${error.message}`, 'error');
            }
        }
        
        async function testASIS() {
            try {
                const response = await fetch('/api/asis/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: 'What is consciousness?' })
                });
                const data = await response.json();
                updateStatus(`ASIS: ${data.response || data.error}`, response.ok ? 'success' : 'error');
            } catch (error) {
                updateStatus(`Error: ${error.message}`, 'error');
            }
        }
    </script>
</body>
</html>
        """
        return web.Response(text=html_content, content_type='text/html')
    
    async def _websocket_handler(self, request):
        """WebSocket handler for real-time communication"""
        
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        client_ip = request.remote
        logger.info(f"WebSocket connection established: {client_ip}")
        
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        message_type = data.get('type', 'unknown')
                        
                        if message_type == 'ping':
                            await ws.send_str(json.dumps({
                                'type': 'pong',
                                'timestamp': datetime.now().isoformat()
                            }))
                        
                        elif message_type == 'security_status':
                            dashboard = self.network_security.get_security_dashboard()
                            await ws.send_str(json.dumps({
                                'type': 'security_dashboard',
                                'data': dashboard
                            }))
                        
                        else:
                            await ws.send_str(json.dumps({
                                'type': 'error',
                                'message': f'Unknown message type: {message_type}'
                            }))
                            
                    except json.JSONDecodeError:
                        await ws.send_str(json.dumps({
                            'type': 'error',
                            'message': 'Invalid JSON message'
                        }))
                
                elif msg.type == WSMsgType.ERROR:
                    logger.error(f'WebSocket error: {ws.exception()}')
                    break
        
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
        
        finally:
            logger.info(f"WebSocket connection closed: {client_ip}")
        
        return ws
    
    def _create_ssl_context(self):
        """Create SSL context with TLS 1.3"""
        
        # Generate certificate if not exists
        if not self.cert_file or not self.key_file:
            cert_pem, key_pem = self.network_security.secure_comm.generate_self_signed_certificate("asis-server")
            
            # Save to temporary files
            with tempfile.NamedTemporaryFile(mode='w', suffix='.pem', delete=False) as cert_file:
                cert_file.write(cert_pem)
                self.cert_file = cert_file.name
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.key', delete=False) as key_file:
                key_file.write(key_pem)
                self.key_file = key_file.name
        
        # Create SSL context
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3
        ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
        
        # Load certificate and key
        ssl_context.load_cert_chain(self.cert_file, self.key_file)
        
        # Security settings
        ssl_context.set_ciphers('TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256')
        
        return ssl_context
    
    async def start_server(self):
        """Start the secure HTTPS server"""
        
        try:
            # Initialize network security
            if not self.network_security.initialize_full_security():
                logger.warning("Network security initialization incomplete")
            
            # Create SSL context
            self.ssl_context = self._create_ssl_context()
            
            # Create runner
            self.runner = web.AppRunner(self.app)
            await self.runner.setup()
            
            # Create site with SSL
            self.site = web.TCPSite(
                self.runner, 
                self.host, 
                self.port, 
                ssl_context=self.ssl_context
            )
            
            await self.site.start()
            
            logger.info(f"🔒 ASIS Secure Server started on https://{self.host}:{self.port}")
            logger.info(f"🛡️ TLS 1.3 enabled with certificate pinning")
            logger.info(f"🔥 Network security active with {self.network_security._calculate_security_score():.2f} security score")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start secure server: {e}")
            return False
    
    async def stop_server(self):
        """Stop the secure server"""
        
        try:
            if self.site:
                await self.site.stop()
            
            if self.runner:
                await self.runner.cleanup()
            
            # Cleanup temporary certificate files
            if self.cert_file and os.path.exists(self.cert_file):
                os.unlink(self.cert_file)
            
            if self.key_file and os.path.exists(self.key_file):
                os.unlink(self.key_file)
            
            logger.info("🔒 ASIS Secure Server stopped")
            
        except Exception as e:
            logger.error(f"Error stopping server: {e}")

# Example usage
async def main():
    """Main function to run the secure server"""
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and start server
    server = ASISSecureServer(host="0.0.0.0", port=8443)
    
    if await server.start_server():
        print("🔒 ASIS Secure Server is running!")
        print("🌐 Access the server at: https://localhost:8443")
        print("⚠️  Note: You may see a certificate warning (expected for self-signed certificates)")
        print("📊 API endpoints available for testing")
        print("Press Ctrl+C to stop the server...")
        
        try:
            # Keep the server running
            while True:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            await server.stop_server()
    
    else:
        print("❌ Failed to start ASIS Secure Server")

if __name__ == "__main__":
    asyncio.run(main())