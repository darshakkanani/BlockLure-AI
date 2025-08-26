import socket
import threading
import struct
from datetime import datetime

class HoneyMySQL:
    def __init__(self, config, logger, geolocation, firewall):
        self.config = config
        self.logger = logger
        self.geolocation = geolocation
        self.firewall = firewall
        self.running = False
        self.server_socket = None
        self.version = self.config['honeypot']['services']['mysql']['version']
    
    def start(self):
        """Start the MySQL honeypot"""
        if not self.config['honeypot']['services']['mysql']['enabled']:
            return
        
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            bind_ip = self.config['honeypot']['bind_ip']
            port = self.config['honeypot']['services']['mysql']['port']
            
            self.server_socket.bind((bind_ip, port))
            self.server_socket.listen(10)
            
            self.running = True
            self.logger.info(f"MySQL Honeypot started on {bind_ip}:{port}")
            
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
                        self.logger.error(f"MySQL accept error: {e}")
                        
        except Exception as e:
            self.logger.error(f"MySQL honeypot failed to start: {e}")
    
    def handle_client(self, client_socket, client_address):
        """Handle MySQL client connection"""
        ip_address = client_address[0]
        
        # Log connection
        self.logger.log_connection({
            'service': 'mysql',
            'ip': ip_address,
            'port': client_address[1],
            'timestamp': datetime.now().isoformat()
        })
        
        try:
            client_socket.settimeout(30)
            
            # Send MySQL handshake packet
            handshake = self.create_handshake_packet()
            client_socket.send(handshake)
            
            # Read authentication response
            auth_data = client_socket.recv(1024)
            if auth_data:
                self.process_auth_attempt(ip_address, auth_data)
                
                # Send authentication error
                error_packet = self.create_error_packet("Access denied for user")
                client_socket.send(error_packet)
                
        except socket.timeout:
            self.logger.debug(f"MySQL timeout from {ip_address}")
        except Exception as e:
            self.logger.debug(f"MySQL connection error from {ip_address}: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass
    
    def create_handshake_packet(self):
        """Create MySQL handshake initialization packet"""
        # MySQL Protocol Version 10
        protocol_version = 10
        server_version = f"{self.version}\x00"
        connection_id = 12345
        auth_plugin_data_part_1 = b"12345678"  # 8 bytes
        filler = 0
        capability_flags_1 = 0xf7df  # Lower 16 bits
        character_set = 8  # latin1_swedish_ci
        status_flags = 2  # SERVER_STATUS_AUTOCOMMIT
        capability_flags_2 = 0x0000  # Upper 16 bits
        auth_plugin_data_len = 21
        reserved = b"\x00" * 10
        auth_plugin_data_part_2 = b"123456789012\x00"  # 13 bytes including null terminator
        auth_plugin_name = b"mysql_native_password\x00"
        
        # Build packet
        payload = struct.pack('<B', protocol_version)
        payload += server_version.encode()
        payload += struct.pack('<I', connection_id)
        payload += auth_plugin_data_part_1
        payload += struct.pack('<B', filler)
        payload += struct.pack('<H', capability_flags_1)
        payload += struct.pack('<B', character_set)
        payload += struct.pack('<H', status_flags)
        payload += struct.pack('<H', capability_flags_2)
        payload += struct.pack('<B', auth_plugin_data_len)
        payload += reserved
        payload += auth_plugin_data_part_2
        payload += auth_plugin_name
        
        # Add packet header (length + sequence)
        packet_length = len(payload)
        header = struct.pack('<I', packet_length)[:-1] + b'\x00'  # 3 bytes length + 1 byte sequence
        
        return header + payload
    
    def create_error_packet(self, message):
        """Create MySQL error packet"""
        error_code = 1045  # ER_ACCESS_DENIED_ERROR
        sql_state = b"28000"
        error_message = message.encode()
        
        payload = struct.pack('<B', 0xff)  # Error packet header
        payload += struct.pack('<H', error_code)
        payload += b'#'  # SQL state marker
        payload += sql_state
        payload += error_message
        
        # Add packet header
        packet_length = len(payload)
        header = struct.pack('<I', packet_length)[:-1] + b'\x01'  # 3 bytes length + sequence 1
        
        return header + payload
    
    def process_auth_attempt(self, ip_address, auth_data):
        """Process MySQL authentication attempt"""
        try:
            # Parse authentication packet (simplified)
            if len(auth_data) < 4:
                return
            
            # Skip packet header (4 bytes)
            data = auth_data[4:]
            
            if len(data) < 32:
                return
            
            # Parse client capabilities and other fields
            capability_flags = struct.unpack('<I', data[0:4])[0]
            max_packet_size = struct.unpack('<I', data[4:8])[0]
            character_set = data[8]
            
            # Skip reserved bytes (23 bytes)
            username_start = 32
            
            # Extract username (null-terminated)
            username_end = data.find(b'\x00', username_start)
            if username_end == -1:
                username = "unknown"
            else:
                username = data[username_start:username_end].decode('utf-8', errors='ignore')
            
            # Extract password hash length and hash
            password_info = "encrypted"
            if username_end != -1 and username_end + 1 < len(data):
                auth_response_len = data[username_end + 1]
                if auth_response_len > 0 and username_end + 2 + auth_response_len <= len(data):
                    password_hash = data[username_end + 2:username_end + 2 + auth_response_len]
                    password_info = password_hash.hex()
            
            # Log the authentication attempt
            attack_data = {
                'service': 'mysql',
                'ip': ip_address,
                'username': username,
                'password_hash': password_info,
                'client_capabilities': hex(capability_flags),
                'timestamp': datetime.now().isoformat()
            }
            
            # Add geolocation data
            if self.geolocation:
                threat_intel = self.geolocation.get_threat_intel(ip_address)
                attack_data.update(threat_intel)
            
            self.logger.log_attack(attack_data)
            
            # Block IP if auto-blocking is enabled
            if self.firewall and self.config['firewall']['auto_block']:
                self.firewall.block_ip(ip_address, f"MySQL login attempt: {username}")
                
        except Exception as e:
            self.logger.debug(f"MySQL auth parsing error: {e}")
            
            # Still log the attempt even if parsing failed
            attack_data = {
                'service': 'mysql',
                'ip': ip_address,
                'raw_data': auth_data[:100].hex(),
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
            if self.geolocation:
                threat_intel = self.geolocation.get_threat_intel(ip_address)
                attack_data.update(threat_intel)
            
            self.logger.log_attack(attack_data)
    
    def stop(self):
        """Stop the MySQL honeypot"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        self.logger.info("MySQL Honeypot stopped")
