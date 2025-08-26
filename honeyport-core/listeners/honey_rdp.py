import socket
import threading
import struct
from datetime import datetime

class HoneyRDP:
    def __init__(self, config, logger, geolocation, firewall):
        self.config = config
        self.logger = logger
        self.geolocation = geolocation
        self.firewall = firewall
        self.running = False
        self.server_socket = None
    
    def start(self):
        """Start the RDP honeypot"""
        if not self.config['honeypot']['services']['rdp']['enabled']:
            return
        
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            bind_ip = self.config['honeypot']['bind_ip']
            port = self.config['honeypot']['services']['rdp']['port']
            
            self.server_socket.bind((bind_ip, port))
            self.server_socket.listen(10)
            
            self.running = True
            self.logger.info(f"RDP Honeypot started on {bind_ip}:{port}")
            
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
                        self.logger.error(f"RDP accept error: {e}")
                        
        except Exception as e:
            self.logger.error(f"RDP honeypot failed to start: {e}")
    
    def handle_client(self, client_socket, client_address):
        """Handle RDP client connection"""
        ip_address = client_address[0]
        
        # Log connection
        self.logger.log_connection({
            'service': 'rdp',
            'ip': ip_address,
            'port': client_address[1],
            'timestamp': datetime.now().isoformat()
        })
        
        try:
            client_socket.settimeout(30)
            
            # Read initial RDP connection request
            data = client_socket.recv(1024)
            if not data:
                return
            
            # Log the RDP attempt
            self.log_rdp_attempt(ip_address, data)
            
            # Send RDP connection response (fake handshake)
            response = self.create_rdp_response()
            client_socket.send(response)
            
            # Try to read more data for credential attempts
            try:
                more_data = client_socket.recv(1024)
                if more_data:
                    self.analyze_rdp_data(ip_address, more_data)
            except:
                pass
                
        except socket.timeout:
            self.logger.debug(f"RDP timeout from {ip_address}")
        except Exception as e:
            self.logger.debug(f"RDP connection error from {ip_address}: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass
    
    def log_rdp_attempt(self, ip_address, data):
        """Log RDP connection attempt"""
        attack_data = {
            'service': 'rdp',
            'ip': ip_address,
            'data_length': len(data),
            'data_hex': data[:100].hex(),  # First 100 bytes as hex
            'timestamp': datetime.now().isoformat()
        }
        
        # Add geolocation data
        if self.geolocation:
            threat_intel = self.geolocation.get_threat_intel(ip_address)
            attack_data.update(threat_intel)
        
        self.logger.log_attack(attack_data)
        
        # Block IP if auto-blocking is enabled
        if self.firewall and self.config['firewall']['auto_block']:
            self.firewall.block_ip(ip_address, "RDP connection attempt")
    
    def analyze_rdp_data(self, ip_address, data):
        """Analyze RDP data for credential attempts"""
        try:
            # Look for potential username/password patterns
            data_str = data.decode('utf-8', errors='ignore')
            
            # Simple pattern matching for common RDP authentication
            if any(keyword in data_str.lower() for keyword in ['administrator', 'admin', 'user', 'guest']):
                attack_data = {
                    'service': 'rdp',
                    'ip': ip_address,
                    'type': 'credential_attempt',
                    'data_sample': data_str[:200],  # First 200 chars
                    'timestamp': datetime.now().isoformat()
                }
                
                # Add geolocation data
                if self.geolocation:
                    threat_intel = self.geolocation.get_threat_intel(ip_address)
                    attack_data.update(threat_intel)
                
                self.logger.log_attack(attack_data)
                
        except Exception as e:
            self.logger.debug(f"RDP data analysis error: {e}")
    
    def create_rdp_response(self):
        """Create a fake RDP handshake response"""
        # This is a simplified RDP response
        # In a real implementation, you'd need proper RDP protocol handling
        
        # RDP Connection Response (simplified)
        response = bytearray([
            0x03, 0x00, 0x00, 0x13,  # TPKT Header
            0x0e, 0xd0, 0x00, 0x00,  # X.224 Connection Confirm
            0x12, 0x34, 0x00, 0x02,  # RDP specific data
            0x1f, 0x08, 0x00, 0x00,
            0x00, 0x00, 0x00
        ])
        
        return bytes(response)
    
    def stop(self):
        """Stop the RDP honeypot"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        self.logger.info("RDP Honeypot stopped")
