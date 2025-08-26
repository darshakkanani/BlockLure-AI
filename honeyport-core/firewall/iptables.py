import subprocess
import ipaddress
import time
from datetime import datetime, timedelta

class IPTablesManager:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.blocked_ips = {}
        self.chain_name = "HONEYPORT_BLOCK"
        self.setup_chain()
    
    def setup_chain(self):
        """Create custom iptables chain for honeypot blocking"""
        try:
            # Create chain if it doesn't exist
            subprocess.run([
                'iptables', '-t', 'filter', '-N', self.chain_name
            ], capture_output=True, check=False)
            
            # Insert jump rule to our chain in INPUT chain
            subprocess.run([
                'iptables', '-t', 'filter', '-I', 'INPUT', '-j', self.chain_name
            ], capture_output=True, check=False)
            
            self.logger.info(f"IPTables chain {self.chain_name} initialized")
        except Exception as e:
            self.logger.error(f"Failed to setup iptables chain: {e}")
    
    def block_ip(self, ip_address, reason="Honeypot attack detected"):
        """Block an IP address using iptables"""
        if not self.config['firewall']['enabled']:
            return False
        
        # Check if IP is whitelisted
        if self.is_whitelisted(ip_address):
            self.logger.info(f"IP {ip_address} is whitelisted, not blocking")
            return False
        
        # Check if already blocked
        if ip_address in self.blocked_ips:
            self.logger.debug(f"IP {ip_address} already blocked")
            return True
        
        try:
            # Add iptables rule to drop packets from this IP
            cmd = [
                'iptables', '-t', 'filter', '-I', self.chain_name,
                '-s', ip_address, '-j', 'DROP'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Record the block
            block_time = datetime.now()
            self.blocked_ips[ip_address] = {
                'blocked_at': block_time,
                'reason': reason,
                'expires_at': block_time + timedelta(seconds=self.config['firewall']['block_duration'])
            }
            
            self.logger.log_block(ip_address, reason)
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to block IP {ip_address}: {e.stderr}")
            return False
        except Exception as e:
            self.logger.error(f"Error blocking IP {ip_address}: {e}")
            return False
    
    def unblock_ip(self, ip_address):
        """Unblock an IP address"""
        if ip_address not in self.blocked_ips:
            return False
        
        try:
            # Remove iptables rule
            cmd = [
                'iptables', '-t', 'filter', '-D', self.chain_name,
                '-s', ip_address, '-j', 'DROP'
            ]
            
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Remove from blocked list
            del self.blocked_ips[ip_address]
            
            self.logger.info(f"Unblocked IP: {ip_address}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to unblock IP {ip_address}: {e.stderr}")
            return False
        except Exception as e:
            self.logger.error(f"Error unblocking IP {ip_address}: {e}")
            return False
    
    def is_whitelisted(self, ip_address):
        """Check if IP is in whitelist"""
        try:
            ip = ipaddress.ip_address(ip_address)
            for whitelist_entry in self.config['firewall']['whitelist']:
                if '/' in whitelist_entry:
                    # CIDR notation
                    network = ipaddress.ip_network(whitelist_entry, strict=False)
                    if ip in network:
                        return True
                else:
                    # Single IP
                    if str(ip) == whitelist_entry:
                        return True
            return False
        except Exception:
            return False
    
    def cleanup_expired_blocks(self):
        """Remove expired IP blocks"""
        current_time = datetime.now()
        expired_ips = []
        
        for ip, block_info in self.blocked_ips.items():
            if current_time > block_info['expires_at']:
                expired_ips.append(ip)
        
        for ip in expired_ips:
            self.unblock_ip(ip)
            self.logger.info(f"Expired block removed for IP: {ip}")
    
    def get_blocked_ips(self):
        """Get list of currently blocked IPs"""
        return dict(self.blocked_ips)
    
    def flush_blocks(self):
        """Remove all honeypot blocks"""
        try:
            # Flush our custom chain
            subprocess.run([
                'iptables', '-t', 'filter', '-F', self.chain_name
            ], capture_output=True, check=True)
            
            self.blocked_ips.clear()
            self.logger.info("All honeypot blocks cleared")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to flush blocks: {e}")
            return False
    
    def get_stats(self):
        """Get firewall statistics"""
        return {
            'total_blocked': len(self.blocked_ips),
            'active_blocks': len([
                ip for ip, info in self.blocked_ips.items()
                if datetime.now() < info['expires_at']
            ]),
            'blocked_ips': list(self.blocked_ips.keys())
        }
    
    def cleanup(self):
        """Cleanup iptables rules on shutdown"""
        try:
            # Remove jump rule from INPUT chain
            subprocess.run([
                'iptables', '-t', 'filter', '-D', 'INPUT', '-j', self.chain_name
            ], capture_output=True, check=False)
            
            # Flush and delete our chain
            subprocess.run([
                'iptables', '-t', 'filter', '-F', self.chain_name
            ], capture_output=True, check=False)
            
            subprocess.run([
                'iptables', '-t', 'filter', '-X', self.chain_name
            ], capture_output=True, check=False)
            
            self.logger.info("IPTables cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during iptables cleanup: {e}")
