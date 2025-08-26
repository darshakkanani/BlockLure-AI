from datetime import datetime
import sqlite3

class Attack:
    def __init__(self, service, ip_address, timestamp=None, **kwargs):
        self.service = service
        self.ip_address = ip_address
        self.timestamp = timestamp or datetime.now().isoformat()
        self.country = kwargs.get('country')
        self.city = kwargs.get('city')
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')
        self.threat_score = kwargs.get('threat_score', 0)
        self.attack_type = kwargs.get('attack_type')
        self.details = kwargs.get('details')
        self.blocked = kwargs.get('blocked', False)
    
    def to_dict(self):
        return {
            'service': self.service,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp,
            'country': self.country,
            'city': self.city,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'threat_score': self.threat_score,
            'attack_type': self.attack_type,
            'details': self.details,
            'blocked': self.blocked
        }

class Connection:
    def __init__(self, service, ip_address, port, timestamp=None, **kwargs):
        self.service = service
        self.ip_address = ip_address
        self.port = port
        self.timestamp = timestamp or datetime.now().isoformat()
        self.details = kwargs.get('details')
    
    def to_dict(self):
        return {
            'service': self.service,
            'ip_address': self.ip_address,
            'port': self.port,
            'timestamp': self.timestamp,
            'details': self.details
        }

class BlockedIP:
    def __init__(self, ip_address, reason, blocked_at=None, expires_at=None, active=True):
        self.ip_address = ip_address
        self.reason = reason
        self.blocked_at = blocked_at or datetime.now().isoformat()
        self.expires_at = expires_at
        self.active = active
    
    def to_dict(self):
        return {
            'ip_address': self.ip_address,
            'reason': self.reason,
            'blocked_at': self.blocked_at,
            'expires_at': self.expires_at,
            'active': self.active
        }
