import subprocess
import platform
import ipaddress
from datetime import datetime, timedelta

class WindowsFirewallManager:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.blocked_ips = {}
        self.rule_prefix = "HoneyPort_Block_"
        
        if platform.system() != "Windows":
            self.logger.warning("Windows Firewall manager loaded on non-Windows system")
    
    def block_ip(self, ip_address, reason="Honeypot attack detected"):
        """Block an IP address using Windows Firewall"""
        if not self.config['firewall']['enabled']:
            return False
        
        if platform.system() != "Windows":
            self.logger.error("Windows Firewall only works on Windows systems")
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
            rule_name = f"{self.rule_prefix}{ip_address.replace('.', '_')}"
            
            # Create Windows Firewall rule to block the IP
            cmd = [
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                f'name={rule_name}',
                'dir=in',
                'action=block',
                f'remoteip={ip_address}',
                'protocol=any'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Record the block
            block_time = datetime.now()
            self.blocked_ips[ip_address] = {
                'blocked_at': block_time,
                'reason': reason,
                'rule_name': rule_name,
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
        
        if platform.system() != "Windows":
            return False
        
        try:
            rule_name = self.blocked_ips[ip_address]['rule_name']
            
            # Remove Windows Firewall rule
            cmd = [
                'netsh', 'advfirewall', 'firewall', 'delete', 'rule',
                f'name={rule_name}'
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
        if platform.system() != "Windows":
            return False
        
        try:
            # Remove all rules with our prefix
            for ip in list(self.blocked_ips.keys()):
                self.unblock_ip(ip)
            
            self.logger.info("All honeypot blocks cleared")
            return True
            
        except Exception as e:
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
        """Cleanup firewall rules on shutdown"""
        try:
            self.flush_blocks()
            self.logger.info("Windows Firewall cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during Windows Firewall cleanup: {e}")
