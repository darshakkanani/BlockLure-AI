import socket
import threading
import urllib.parse
import json
from datetime import datetime
import re

class HoneyHTTP:
    def __init__(self, config, logger, geolocation, firewall):
        self.config = config
        self.logger = logger
        self.geolocation = geolocation
        self.firewall = firewall
        self.running = False
        self.server_socket = None
        
        # Common attack patterns
        self.attack_patterns = [
            r'/admin',
            r'/wp-admin',
            r'/phpmyadmin',
            r'/\.env',
            r'/config\.php',
            r'/shell\.php',
            r'/cmd\.php',
            r'/backdoor',
            r'/webshell',
            r'<script',
            r'union.*select',
            r'drop.*table',
            r'exec\(',
            r'system\(',
            r'passthru\(',
            r'shell_exec\(',
        ]
    
    def start(self):
        """Start the HTTP honeypot"""
        if not self.config['honeypot']['services']['http']['enabled']:
            return
        
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            bind_ip = self.config['honeypot']['bind_ip']
            port = self.config['honeypot']['services']['http']['port']
            
            self.server_socket.bind((bind_ip, port))
            self.server_socket.listen(10)
            
            self.running = True
            self.logger.info(f"HTTP Honeypot started on {bind_ip}:{port}")
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except Exception as e:
                    if self.running:
                        self.logger.error(f"HTTP accept error: {e}")
                        
        except Exception as e:
            self.logger.error(f"HTTP honeypot failed to start: {e}")
    
    def handle_client(self, client_socket, client_address):
        """Handle HTTP client connection"""
        ip_address = client_address[0]
        
        try:
            # Set timeout for client socket
            client_socket.settimeout(30)
            
            # Read HTTP request
            request_data = b""
            while b"\r\n\r\n" not in request_data:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                request_data += chunk
                
                # Prevent excessive data
                if len(request_data) > 8192:
                    break
            
            if request_data:
                self.process_request(client_socket, ip_address, request_data)
                
        except socket.timeout:
            self.logger.debug(f"HTTP timeout from {ip_address}")
        except Exception as e:
            self.logger.debug(f"HTTP connection error from {ip_address}: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass
    
    def process_request(self, client_socket, ip_address, request_data):
        """Process HTTP request and detect attacks"""
        try:
            request_str = request_data.decode('utf-8', errors='ignore')
            lines = request_str.split('\r\n')
            
            if not lines:
                return
            
            # Parse request line
            request_line = lines[0]
            parts = request_line.split(' ')
            
            if len(parts) < 3:
                return
            
            method = parts[0]
            path = parts[1]
            version = parts[2]
            
            # Parse headers
            headers = {}
            for line in lines[1:]:
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip().lower()] = value.strip()
            
            # Log connection
            self.logger.log_connection({
                'service': 'http',
                'ip': ip_address,
                'method': method,
                'path': path,
                'user_agent': headers.get('user-agent', 'Unknown'),
                'timestamp': datetime.now().isoformat()
            })
            
            # Check for attack patterns
            is_attack = self.detect_attack(method, path, headers, request_str)
            
            if is_attack:
                self.log_attack(ip_address, method, path, headers, request_str)
            
            # Send response
            response = self.generate_response(path, method, headers, is_attack)
            client_socket.send(response.encode())
            
        except Exception as e:
            self.logger.debug(f"HTTP request processing error: {e}")
    
    def detect_attack(self, method, path, headers, full_request):
        """Detect if request contains attack patterns"""
        # Check URL path for suspicious patterns
        for pattern in self.attack_patterns:
            if re.search(pattern, path, re.IGNORECASE):
                return True
        
        # Check for SQL injection in parameters
        if '?' in path:
            query_string = path.split('?', 1)[1]
            if re.search(r'(union.*select|drop.*table|insert.*into)', query_string, re.IGNORECASE):
                return True
        
        # Check for XSS attempts
        if re.search(r'<script|javascript:|onload=|onerror=', full_request, re.IGNORECASE):
            return True
        
        # Check for directory traversal
        if '../' in path or '..\\' in path:
            return True
        
        # Check for suspicious user agents
        user_agent = headers.get('user-agent', '').lower()
        suspicious_agents = ['sqlmap', 'nikto', 'nmap', 'masscan', 'zap', 'burp']
        for agent in suspicious_agents:
            if agent in user_agent:
                return True
        
        # Check for common exploit attempts
        exploit_patterns = [
            r'eval\(',
            r'base64_decode',
            r'file_get_contents',
            r'fopen\(',
            r'include\(',
            r'require\(',
        ]
        
        for pattern in exploit_patterns:
            if re.search(pattern, full_request, re.IGNORECASE):
                return True
        
        return False
    
    def log_attack(self, ip_address, method, path, headers, full_request):
        """Log HTTP attack attempt"""
        attack_data = {
            'service': 'http',
            'ip': ip_address,
            'method': method,
            'path': path,
            'user_agent': headers.get('user-agent', 'Unknown'),
            'referer': headers.get('referer', ''),
            'request_size': len(full_request),
            'timestamp': datetime.now().isoformat()
        }
        
        # Add geolocation data
        if self.geolocation:
            threat_intel = self.geolocation.get_threat_intel(ip_address)
            attack_data.update(threat_intel)
        
        self.logger.log_attack(attack_data)
        
        # Block IP if auto-blocking is enabled
        if self.firewall and self.config['firewall']['auto_block']:
            self.firewall.block_ip(ip_address, f"HTTP attack: {method} {path}")
    
    def generate_response(self, path, method, headers, is_attack):
        """Generate HTTP response"""
        server_name = self.config['honeypot']['services']['http']['server_name']
        
        if is_attack:
            # Return 404 for attacks to not reveal honeypot
            status = "404 Not Found"
            body = "<html><body><h1>404 Not Found</h1><p>The requested resource was not found.</p></body></html>"
        else:
            # Return fake website for normal requests
            if path == '/' or path == '/index.html':
                status = "200 OK"
                body = self.get_fake_homepage()
            elif path == '/login' or path == '/admin':
                status = "200 OK"
                body = self.get_fake_login_page()
            elif path.endswith('.php'):
                status = "200 OK"
                body = self.get_fake_php_page()
            else:
                status = "404 Not Found"
                body = "<html><body><h1>404 Not Found</h1></body></html>"
        
        response = f"""HTTP/1.1 {status}\r
Server: {server_name}\r
Content-Type: text/html\r
Content-Length: {len(body)}\r
Connection: close\r
\r
{body}"""
        
        return response
    
    def get_fake_homepage(self):
        """Generate fake homepage"""
        return """<!DOCTYPE html>
<html>
<head>
    <title>Welcome to Our Website</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { background: #f0f0f0; padding: 20px; }
        .content { padding: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Corporate Website</h1>
        <p>Your trusted business partner</p>
    </div>
    <div class="content">
        <h2>About Us</h2>
        <p>We are a leading company in our industry, providing excellent services to our clients worldwide.</p>
        <h2>Services</h2>
        <ul>
            <li>Consulting</li>
            <li>Development</li>
            <li>Support</li>
        </ul>
        <p><a href="/login">Admin Login</a></p>
    </div>
</body>
</html>"""
    
    def get_fake_login_page(self):
        """Generate fake login page"""
        return """<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .login-form { max-width: 400px; margin: 0 auto; padding: 20px; border: 1px solid #ccc; }
        input { width: 100%; padding: 10px; margin: 10px 0; }
        button { background: #007cba; color: white; padding: 10px 20px; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="login-form">
        <h2>Administrator Login</h2>
        <form method="post" action="/login">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <p><small>Please contact IT support if you forgot your credentials.</small></p>
    </div>
</body>
</html>"""
    
    def get_fake_php_page(self):
        """Generate fake PHP page"""
        return """<!DOCTYPE html>
<html>
<head>
    <title>PHP Info</title>
</head>
<body>
    <h1>PHP Configuration</h1>
    <p>PHP Version: 7.4.3</p>
    <p>Server: Apache/2.4.41 (Ubuntu)</p>
    <p>Document Root: /var/www/html</p>
    <p>For security reasons, detailed PHP information is not displayed.</p>
</body>
</html>"""
    
    def stop(self):
        """Stop the HTTP honeypot"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        self.logger.info("HTTP Honeypot stopped")
