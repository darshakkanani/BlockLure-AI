#!/usr/bin/env python3
import yaml
import threading
import signal
import sys
import os
import platform
import sqlite3
from datetime import datetime

# Import honeypot components
from logger import HoneypotLogger
from geolocation import GeoLocator
from listeners.honey_ssh import HoneySSH
from listeners.honey_http import HoneyHTTP
from listeners.honey_rdp import HoneyRDP
from listeners.honey_mysql import HoneyMySQL

# Import firewall managers
if platform.system() == "Windows":
    from firewall.windows_firewall import WindowsFirewallManager as FirewallManager
else:
    from firewall.iptables import IPTablesManager as FirewallManager

class HoneyPortCore:
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self.config = None
        self.logger = None
        self.geolocation = None
        self.firewall = None
        self.services = {}
        self.running = False
        
        # Load configuration
        self.load_config()
        
        # Initialize components
        self.setup_database()
        self.setup_logger()
        self.setup_geolocation()
        self.setup_firewall()
        self.setup_services()
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def load_config(self):
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            print(f"Configuration loaded from {self.config_path}")
        except FileNotFoundError:
            print(f"Error: Configuration file {self.config_path} not found")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing configuration file: {e}")
            sys.exit(1)
    
    def setup_database(self):
        """Initialize SQLite database for storing attack data"""
        db_path = self.config['database']['path']
        db_dir = os.path.dirname(db_path)
        
        # Create directory if it doesn't exist
        os.makedirs(db_dir, exist_ok=True)
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create attacks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attacks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    service TEXT NOT NULL,
                    ip_address TEXT NOT NULL,
                    country TEXT,
                    city TEXT,
                    latitude REAL,
                    longitude REAL,
                    threat_score INTEGER,
                    attack_type TEXT,
                    details TEXT,
                    blocked BOOLEAN DEFAULT FALSE
                )
            ''')
            
            # Create connections table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS connections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    service TEXT NOT NULL,
                    ip_address TEXT NOT NULL,
                    port INTEGER,
                    details TEXT
                )
            ''')
            
            # Create blocked_ips table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS blocked_ips (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address TEXT UNIQUE NOT NULL,
                    blocked_at TEXT NOT NULL,
                    reason TEXT,
                    expires_at TEXT,
                    active BOOLEAN DEFAULT TRUE
                )
            ''')
            
            conn.commit()
            conn.close()
            
            print(f"Database initialized at {db_path}")
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            sys.exit(1)
    
    def setup_logger(self):
        """Initialize logging system"""
        self.logger = HoneypotLogger(self.config)
        self.logger.info("HoneyPort logging system initialized")
    
    def setup_geolocation(self):
        """Initialize geolocation system"""
        self.geolocation = GeoLocator(self.config)
        if self.config['geolocation']['enabled']:
            self.logger.info("Geolocation system initialized")
        else:
            self.logger.info("Geolocation system disabled")
    
    def setup_firewall(self):
        """Initialize firewall management"""
        if self.config['firewall']['enabled']:
            self.firewall = FirewallManager(self.config, self.logger)
            self.logger.info(f"Firewall manager initialized ({platform.system()})")
        else:
            self.logger.info("Firewall integration disabled")
    
    def setup_services(self):
        """Initialize honeypot services"""
        services_config = self.config['honeypot']['services']
        
        # SSH Honeypot
        if services_config['ssh']['enabled']:
            self.services['ssh'] = HoneySSH(self.config, self.logger, self.geolocation, self.firewall)
        
        # HTTP Honeypot
        if services_config['http']['enabled']:
            self.services['http'] = HoneyHTTP(self.config, self.logger, self.geolocation, self.firewall)
        
        # RDP Honeypot
        if services_config['rdp']['enabled']:
            self.services['rdp'] = HoneyRDP(self.config, self.logger, self.geolocation, self.firewall)
        
        # MySQL Honeypot
        if services_config['mysql']['enabled']:
            self.services['mysql'] = HoneyMySQL(self.config, self.logger, self.geolocation, self.firewall)
        
        self.logger.info(f"Initialized {len(self.services)} honeypot services")
    
    def start(self):
        """Start all honeypot services"""
        if self.running:
            return
        
        self.running = True
        self.logger.info("Starting HoneyPort system...")
        
        # Start each service in its own thread
        for service_name, service in self.services.items():
            thread = threading.Thread(target=service.start, name=f"{service_name}_thread")
            thread.daemon = True
            thread.start()
            self.logger.info(f"Started {service_name} service")
        
        # Start cleanup thread for expired firewall blocks
        if self.firewall:
            cleanup_thread = threading.Thread(target=self.cleanup_loop, name="cleanup_thread")
            cleanup_thread.daemon = True
            cleanup_thread.start()
        
        self.logger.info("HoneyPort system started successfully")
        
        # Keep main thread alive
        try:
            while self.running:
                threading.Event().wait(1)
        except KeyboardInterrupt:
            pass
    
    def cleanup_loop(self):
        """Periodic cleanup of expired firewall blocks"""
        import time
        while self.running:
            try:
                if self.firewall:
                    self.firewall.cleanup_expired_blocks()
                time.sleep(300)  # Run every 5 minutes
            except Exception as e:
                self.logger.error(f"Cleanup loop error: {e}")
                time.sleep(60)  # Wait 1 minute before retry
    
    def stop(self):
        """Stop all honeypot services"""
        if not self.running:
            return
        
        self.logger.info("Stopping HoneyPort system...")
        self.running = False
        
        # Stop all services
        for service_name, service in self.services.items():
            try:
                service.stop()
                self.logger.info(f"Stopped {service_name} service")
            except Exception as e:
                self.logger.error(f"Error stopping {service_name}: {e}")
        
        # Cleanup firewall rules
        if self.firewall:
            try:
                self.firewall.cleanup()
            except Exception as e:
                self.logger.error(f"Firewall cleanup error: {e}")
        
        # Close geolocation database
        if self.geolocation:
            try:
                self.geolocation.close()
            except Exception as e:
                self.logger.error(f"Geolocation cleanup error: {e}")
        
        self.logger.info("HoneyPort system stopped")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\nReceived signal {signum}, shutting down...")
        self.stop()
        sys.exit(0)
    
    def get_stats(self):
        """Get system statistics"""
        stats = {
            'running': self.running,
            'services': list(self.services.keys()),
            'firewall_enabled': self.config['firewall']['enabled'],
            'geolocation_enabled': self.config['geolocation']['enabled']
        }
        
        if self.firewall:
            stats['firewall_stats'] = self.firewall.get_stats()
        
        return stats


def main():
    """Main entry point"""
    print("=" * 50)
    print("BlockLure-AI Advanced Honeypot System")
    print("=" * 50)
    
    # Check if running as root (required for some features)
    if platform.system() != "Windows" and os.geteuid() != 0:
        print("Warning: Not running as root. Some features may not work properly.")
        print("Consider running with sudo for full functionality.")
    
    try:
        # Initialize and start honeypot
        honeypot = HoneyPortCore()
        honeypot.start()
        
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
