import logging
import os
from datetime import datetime
import json
from logging.handlers import RotatingFileHandler

class HoneypotLogger:
    def __init__(self, config):
        self.config = config
        self.setup_logger()
    
    def setup_logger(self):
        """Setup logging configuration"""
        log_dir = os.path.dirname(self.config['logging']['file'])
        os.makedirs(log_dir, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger('honeyport')
        self.logger.setLevel(getattr(logging, self.config['logging']['level']))
        
        # Create rotating file handler
        handler = RotatingFileHandler(
            self.config['logging']['file'],
            maxBytes=self._parse_size(self.config['logging']['max_size']),
            backupCount=self.config['logging']['backup_count']
        )
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(handler)
        
        # Also log to console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def _parse_size(self, size_str):
        """Parse size string like '10MB' to bytes"""
        size_str = size_str.upper()
        if size_str.endswith('MB'):
            return int(size_str[:-2]) * 1024 * 1024
        elif size_str.endswith('KB'):
            return int(size_str[:-2]) * 1024
        else:
            return int(size_str)
    
    def log_attack(self, attack_data):
        """Log attack attempt with structured data"""
        attack_log = {
            'timestamp': datetime.now().isoformat(),
            'type': 'ATTACK',
            'data': attack_data
        }
        self.logger.warning(f"ATTACK: {json.dumps(attack_log)}")
    
    def log_connection(self, conn_data):
        """Log connection attempt"""
        conn_log = {
            'timestamp': datetime.now().isoformat(),
            'type': 'CONNECTION',
            'data': conn_data
        }
        self.logger.info(f"CONNECTION: {json.dumps(conn_log)}")
    
    def log_block(self, ip, reason):
        """Log IP blocking action"""
        block_log = {
            'timestamp': datetime.now().isoformat(),
            'type': 'BLOCK',
            'ip': ip,
            'reason': reason
        }
        self.logger.warning(f"BLOCKED: {json.dumps(block_log)}")
        
        # Also write to blocked IPs log
        blocked_log_path = os.path.join(
            os.path.dirname(self.config['logging']['file']),
            'blocked_ips.log'
        )
        with open(blocked_log_path, 'a') as f:
            f.write(f"{datetime.now().isoformat()} - {ip} - {reason}\n")
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
