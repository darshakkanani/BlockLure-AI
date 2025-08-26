import geoip2.database
import geoip2.errors
import requests
import os

class GeoLocator:
    def __init__(self, config):
        self.config = config
        self.reader = None
        self.setup_geolocation()
    
    def setup_geolocation(self):
        """Initialize GeoIP database"""
        if not self.config['geolocation']['enabled']:
            return
        
        db_path = self.config['geolocation']['maxmind_db']
        
        # Download GeoLite2 database if not exists
        if not os.path.exists(db_path):
            self.download_geolite_db(db_path)
        
        try:
            self.reader = geoip2.database.Reader(db_path)
        except Exception as e:
            print(f"Warning: Could not load GeoIP database: {e}")
            print("Geolocation features will be disabled")
    
    def download_geolite_db(self, db_path):
        """Download GeoLite2 database (requires MaxMind account)"""
        print("GeoLite2 database not found.")
        print("Please download from: https://dev.maxmind.com/geoip/geolite2-free-geolocation-data")
        print(f"Place the database at: {db_path}")
    
    def get_location(self, ip_address):
        """Get location information for an IP address"""
        if not self.reader:
            return {
                'country': 'Unknown',
                'city': 'Unknown',
                'latitude': 0.0,
                'longitude': 0.0,
                'isp': 'Unknown'
            }
        
        try:
            response = self.reader.city(ip_address)
            return {
                'country': response.country.name or 'Unknown',
                'city': response.city.name or 'Unknown',
                'latitude': float(response.location.latitude or 0.0),
                'longitude': float(response.location.longitude or 0.0),
                'isp': self.get_isp(ip_address)
            }
        except geoip2.errors.AddressNotFoundError:
            return {
                'country': 'Unknown',
                'city': 'Unknown',
                'latitude': 0.0,
                'longitude': 0.0,
                'isp': 'Unknown'
            }
        except Exception as e:
            return {
                'country': 'Error',
                'city': str(e),
                'latitude': 0.0,
                'longitude': 0.0,
                'isp': 'Unknown'
            }
    
    def get_isp(self, ip_address):
        """Get ISP information (basic implementation)"""
        try:
            # This is a simplified ISP lookup
            # In production, you'd use a proper ISP database
            response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('isp', 'Unknown')
        except:
            pass
        return 'Unknown'
    
    def is_tor_exit(self, ip_address):
        """Check if IP is a Tor exit node (basic implementation)"""
        # This is a simplified check
        # In production, you'd use a proper Tor exit list
        try:
            response = requests.get(
                f"https://check.torproject.org/torbulkexitlist?ip={ip_address}",
                timeout=5
            )
            return ip_address in response.text
        except:
            return False
    
    def get_threat_intel(self, ip_address):
        """Get basic threat intelligence for an IP"""
        location = self.get_location(ip_address)
        
        # Add threat indicators
        threat_score = 0
        indicators = []
        
        # High-risk countries (example)
        high_risk_countries = ['Unknown', 'China', 'Russia', 'North Korea']
        if location['country'] in high_risk_countries:
            threat_score += 30
            indicators.append(f"High-risk country: {location['country']}")
        
        # Check if Tor exit
        if self.is_tor_exit(ip_address):
            threat_score += 50
            indicators.append("Tor exit node")
        
        # Private/Reserved IP ranges
        if self.is_private_ip(ip_address):
            threat_score -= 20
            indicators.append("Private IP range")
        
        return {
            'threat_score': min(threat_score, 100),
            'indicators': indicators,
            'location': location
        }
    
    def is_private_ip(self, ip_address):
        """Check if IP is in private range"""
        import ipaddress
        try:
            ip = ipaddress.ip_address(ip_address)
            return ip.is_private
        except:
            return False
    
    def close(self):
        """Close the GeoIP database"""
        if self.reader:
            self.reader.close()
