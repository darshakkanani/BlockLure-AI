import socket
import threading
import paramiko
import io
import time
from datetime import datetime

class HoneySSH:
    def __init__(self, config, logger, geolocation, firewall):
        self.config = config
        self.logger = logger
        self.geolocation = geolocation
        self.firewall = firewall
        self.running = False
        self.server_socket = None
        
        # Generate server key
        self.host_key = paramiko.RSAKey.generate(2048)
        
        # Common credentials for logging
        self.common_creds = [
            ('admin', 'admin'), ('root', 'root'), ('admin', '123456'),
            ('root', 'password'), ('admin', 'password'), ('user', 'user'),
            ('test', 'test'), ('guest', 'guest'), ('oracle', 'oracle'),
            ('postgres', 'postgres'), ('mysql', 'mysql')
        ]
    
    def start(self):
        """Start the SSH honeypot"""
        if not self.config['honeypot']['services']['ssh']['enabled']:
            return
        
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            bind_ip = self.config['honeypot']['bind_ip']
            port = self.config['honeypot']['services']['ssh']['port']
            
            self.server_socket.bind((bind_ip, port))
            self.server_socket.listen(10)
            
            self.running = True
            self.logger.info(f"SSH Honeypot started on {bind_ip}:{port}")
            
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
                        self.logger.error(f"SSH accept error: {e}")
                        
        except Exception as e:
            self.logger.error(f"SSH honeypot failed to start: {e}")
    
    def handle_client(self, client_socket, client_address):
        """Handle SSH client connection"""
        ip_address = client_address[0]
        
        # Log connection
        self.logger.log_connection({
            'service': 'ssh',
            'ip': ip_address,
            'port': client_address[1],
            'timestamp': datetime.now().isoformat()
        })
        
        try:
            # Create SSH transport
            transport = paramiko.Transport(client_socket)
            transport.add_server_key(self.host_key)
            
            # Set banner
            banner = self.config['honeypot']['services']['ssh']['banner']
            transport.set_subsystem_handler('sftp', paramiko.SFTPServer)
            
            # Start server
            server = SSHServer(self, ip_address)
            transport.start_server(server=server)
            
            # Wait for authentication
            channel = transport.accept(timeout=30)
            if channel is not None:
                self.handle_shell(channel, ip_address)
                
        except Exception as e:
            self.logger.debug(f"SSH connection error from {ip_address}: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass
    
    def handle_shell(self, channel, ip_address):
        """Handle SSH shell session"""
        try:
            # Send fake shell prompt
            channel.send(b"Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-91-generic x86_64)\n")
            channel.send(b"Last login: Mon Jan  1 00:00:00 2024 from 192.168.1.100\n")
            channel.send(b"root@honeypot:~# ")
            
            command_buffer = b""
            
            while True:
                try:
                    data = channel.recv(1024)
                    if not data:
                        break
                    
                    # Handle backspace
                    if data == b'\x7f':
                        if command_buffer:
                            command_buffer = command_buffer[:-1]
                            channel.send(b'\b \b')
                        continue
                    
                    # Handle enter
                    if data in [b'\r', b'\n', b'\r\n']:
                        command = command_buffer.decode('utf-8', errors='ignore').strip()
                        
                        if command:
                            self.log_command(ip_address, command)
                            response = self.process_command(command)
                            channel.send(response.encode() + b"\n")
                        
                        channel.send(b"root@honeypot:~# ")
                        command_buffer = b""
                        continue
                    
                    # Regular character
                    command_buffer += data
                    channel.send(data)  # Echo back
                    
                except socket.timeout:
                    break
                except Exception as e:
                    self.logger.debug(f"SSH shell error: {e}")
                    break
                    
        except Exception as e:
            self.logger.debug(f"SSH shell session error: {e}")
        finally:
            try:
                channel.close()
            except:
                pass
    
    def process_command(self, command):
        """Process SSH commands and return fake responses"""
        command = command.lower().strip()
        
        # Common commands with fake responses
        if command in ['ls', 'ls -la', 'ls -l']:
            return "total 24\ndrwxr-xr-x 3 root root 4096 Jan  1 00:00 .\ndrwxr-xr-x 3 root root 4096 Jan  1 00:00 ..\n-rw-r--r-- 1 root root  220 Jan  1 00:00 .bash_logout\n-rw-r--r-- 1 root root 3771 Jan  1 00:00 .bashrc\n-rw-r--r-- 1 root root  807 Jan  1 00:00 .profile"
        
        elif command == 'pwd':
            return "/root"
        
        elif command == 'whoami':
            return "root"
        
        elif command == 'id':
            return "uid=0(root) gid=0(root) groups=0(root)"
        
        elif command in ['ps', 'ps aux']:
            return "USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\nroot         1  0.0  0.1  19356  1544 ?        Ss   00:00   0:01 /sbin/init\nroot         2  0.0  0.0      0     0 ?        S    00:00   0:00 [kthreadd]"
        
        elif command == 'uname -a':
            return "Linux honeypot 5.4.0-91-generic #102-Ubuntu SMP Fri Nov 5 16:31:28 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux"
        
        elif command.startswith('cat '):
            filename = command[4:].strip()
            return f"cat: {filename}: No such file or directory"
        
        elif command == 'exit':
            return "logout"
        
        else:
            return f"bash: {command}: command not found"
    
    def log_command(self, ip_address, command):
        """Log SSH command execution"""
        attack_data = {
            'service': 'ssh',
            'ip': ip_address,
            'command': command,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add geolocation data
        if self.geolocation:
            threat_intel = self.geolocation.get_threat_intel(ip_address)
            attack_data.update(threat_intel)
        
        self.logger.log_attack(attack_data)
        
        # Block IP if auto-blocking is enabled
        if self.firewall and self.config['firewall']['auto_block']:
            self.firewall.block_ip(ip_address, f"SSH command execution: {command}")
    
    def stop(self):
        """Stop the SSH honeypot"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        self.logger.info("SSH Honeypot stopped")


class SSHServer(paramiko.ServerInterface):
    def __init__(self, honeypot, client_ip):
        self.honeypot = honeypot
        self.client_ip = client_ip
        self.auth_attempts = 0
    
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username, password):
        """Handle password authentication attempts"""
        self.auth_attempts += 1
        
        # Log authentication attempt
        auth_data = {
            'service': 'ssh',
            'ip': self.client_ip,
            'username': username,
            'password': password,
            'attempt': self.auth_attempts,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add geolocation data
        if self.honeypot.geolocation:
            threat_intel = self.honeypot.geolocation.get_threat_intel(self.client_ip)
            auth_data.update(threat_intel)
        
        self.honeypot.logger.log_attack(auth_data)
        
        # Allow common credentials to proceed (for interaction)
        if (username, password) in self.honeypot.common_creds:
            return paramiko.AUTH_SUCCESSFUL
        
        # Block IP after multiple attempts
        if self.auth_attempts >= 3:
            if self.honeypot.firewall and self.honeypot.config['firewall']['auto_block']:
                self.honeypot.firewall.block_ip(
                    self.client_ip, 
                    f"SSH brute force: {self.auth_attempts} attempts"
                )
        
        return paramiko.AUTH_FAILED
    
    def get_allowed_auths(self, username):
        return 'password'
    
    def check_channel_shell_request(self, channel):
        return True
    
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True
