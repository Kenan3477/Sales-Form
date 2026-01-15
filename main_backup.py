from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import hmac
import hashlib
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs

# WSGI Application for Railway Nixpacks
def verify_stripe_signature(payload, signature, endpoint_secret):
    """Verify Stripe webhook signature"""
    if not signature or not endpoint_secret:
        return False
    
    try:
        # Get the signature from header
        sig_header = signature.split(',')
        timestamp = None
        signatures = []
        
        for element in sig_header:
            key, value = element.split('=')
            if key == 't':
                timestamp = value
            elif key == 'v1':
                signatures.append(value)
        
        if not timestamp or not signatures:
            return False
            
        # Create expected signature
        signed_payload = f"{timestamp}.{payload}"
        expected_sig = hmac.new(
            endpoint_secret.encode('utf-8'),
            signed_payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Compare signatures
        return any(hmac.compare_digest(expected_sig, sig) for sig in signatures)
    except Exception:
        return False

def handle_stripe_webhook(event_data):
    """Handle different Stripe webhook events"""
    event_type = event_data.get('type')
    
    if event_type == 'checkout.session.completed':
        session = event_data['data']['object']
        customer_email = session.get('customer_email')
        amount_total = session.get('amount_total', 0) / 100  # Convert from cents
        
        print(f"Payment successful: {customer_email} paid ${amount_total}")
        
        # Log the successful payment
        return {
            "status": "success",
            "message": "Payment processed",
            "customer_email": customer_email,
            "amount": amount_total,
            "is_academic": customer_email.endswith('.edu') if customer_email else False
        }
    
    elif event_type == 'invoice.payment_succeeded':
        invoice = event_data['data']['object']
        customer_email = invoice.get('customer_email')
        amount_paid = invoice.get('amount_paid', 0) / 100
        
        print(f"Subscription payment: {customer_email} paid ${amount_paid}")
        
        return {
            "status": "success",
            "message": "Subscription payment processed",
            "customer_email": customer_email,
            "amount": amount_paid
        }
    
    elif event_type == 'invoice.payment_failed':
        invoice = event_data['data']['object']
        customer_email = invoice.get('customer_email')
        
        print(f"Payment failed for: {customer_email}")
        
        return {
            "status": "failed",
            "message": "Payment failed",
            "customer_email": customer_email
        }
    
    else:
        print(f"Unhandled event type: {event_type}")
        return {
            "status": "ignored",
            "message": f"Event type {event_type} not handled"
        }

def application(environ, start_response):
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']
    
    if method == 'GET':
        if path == '/':
            response_body = json.dumps({"message": "ASIS Research Platform", "status": "running"})
        elif path == '/health':
            response_body = json.dumps({"status": "healthy"})
        else:
            start_response('404 Not Found', [('Content-Type', 'application/json')])
            return [json.dumps({"error": "Not found"}).encode()]
    elif method == 'POST' and path == '/register':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
            data = json.loads(request_body)
            email = data.get('email', '')
            response_body = json.dumps({
                "message": "Registration successful",
                "email": email,
                "is_academic": email.endswith('.edu'),
                "discount": 50 if email.endswith('.edu') else 0
            })
        except:
            start_response('400 Bad Request', [('Content-Type', 'application/json')])
            return [json.dumps({"error": "Invalid JSON"}).encode()]
    elif method == 'POST' and path == '/stripe/webhook':
        try:
            # Get Stripe webhook secret from environment
            webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
            if not webhook_secret:
                start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
                return [json.dumps({"error": "Webhook secret not configured"}).encode()]
            
            # Get request body and signature
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size)
            signature = environ.get('HTTP_STRIPE_SIGNATURE', '')
            
            # Verify signature
            if not verify_stripe_signature(request_body.decode('utf-8'), signature, webhook_secret):
                start_response('400 Bad Request', [('Content-Type', 'application/json')])
                return [json.dumps({"error": "Invalid signature"}).encode()]
            
            # Parse and handle the event
            event_data = json.loads(request_body.decode('utf-8'))
            result = handle_stripe_webhook(event_data)
            
            response_body = json.dumps(result)
            
        except Exception as e:
            print(f"Webhook error: {str(e)}")
            start_response('400 Bad Request', [('Content-Type', 'application/json')])
            return [json.dumps({"error": "Webhook processing failed"}).encode()]
    else:
        start_response('404 Not Found', [('Content-Type', 'application/json')])
        return [json.dumps({"error": "Not found"}).encode()]
    
    start_response('200 OK', [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
        ('Access-Control-Allow-Headers', 'Content-Type')
    ])
    return [response_body.encode()]

# For gunicorn compatibility
app = application

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            response = {"message": "ASIS Research Platform", "status": "running"}
        elif self.path == '/health':
            response = {"status": "healthy"}
        else:
            self.send_response(404)
            self.end_headers()
            return
            
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
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
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
        elif self.path == '/stripe/webhook':
            # Stripe webhook endpoint
            try:
                webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
                if not webhook_secret:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Webhook secret not configured"}).encode())
                    return
                
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                signature = self.headers.get('Stripe-Signature', '')
                
                # Verify signature
                if not verify_stripe_signature(post_data.decode('utf-8'), signature, webhook_secret):
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Invalid signature"}).encode())
                    return
                
                # Process webhook
                event_data = json.loads(post_data.decode('utf-8'))
                result = handle_stripe_webhook(event_data)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                
            except Exception as e:
                print(f"Webhook error: {str(e)}")
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Webhook processing failed"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server():
    port = int(os.environ.get('PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f'ASIS server running on port {port}')
    print(f'Health check: http://0.0.0.0:{port}/health')
    server.serve_forever()

if __name__ == '__main__':
    run_server()
