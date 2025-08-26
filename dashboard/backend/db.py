import sqlite3
import json
from datetime import datetime
from models import Attack, Connection, BlockedIP

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
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
                blocked BOOLEAN DEFAULT FALSE,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
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
                details TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
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
                active BOOLEAN DEFAULT TRUE,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_attacks_ip ON attacks(ip_address)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_attacks_timestamp ON attacks(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_attacks_service ON attacks(service)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_blocked_ips_active ON blocked_ips(active)')
        
        conn.commit()
        conn.close()
    
    def insert_attack(self, attack_data):
        """Insert attack record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO attacks 
            (timestamp, service, ip_address, country, city, latitude, longitude, 
             threat_score, attack_type, details, blocked)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            attack_data.get('timestamp'),
            attack_data.get('service'),
            attack_data.get('ip_address'),
            attack_data.get('country'),
            attack_data.get('city'),
            attack_data.get('latitude'),
            attack_data.get('longitude'),
            attack_data.get('threat_score', 0),
            attack_data.get('attack_type'),
            json.dumps(attack_data.get('details', {})),
            attack_data.get('blocked', False)
        ))
        
        conn.commit()
        attack_id = cursor.lastrowid
        conn.close()
        return attack_id
    
    def insert_connection(self, conn_data):
        """Insert connection record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO connections 
            (timestamp, service, ip_address, port, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            conn_data.get('timestamp'),
            conn_data.get('service'),
            conn_data.get('ip_address'),
            conn_data.get('port'),
            json.dumps(conn_data.get('details', {}))
        ))
        
        conn.commit()
        conn_id = cursor.lastrowid
        conn.close()
        return conn_id
    
    def block_ip(self, ip_address, reason, expires_at=None):
        """Block an IP address"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO blocked_ips 
            (ip_address, blocked_at, reason, expires_at, active)
            VALUES (?, ?, ?, ?, 1)
        ''', (
            ip_address,
            datetime.now().isoformat(),
            reason,
            expires_at
        ))
        
        conn.commit()
        conn.close()
    
    def unblock_ip(self, ip_address):
        """Unblock an IP address"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE blocked_ips 
            SET active = 0 
            WHERE ip_address = ?
        ''', (ip_address,))
        
        conn.commit()
        conn.close()
    
    def get_recent_attacks(self, hours=24, limit=100):
        """Get recent attacks"""
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        conn = self.get_connection()
        attacks = conn.execute('''
            SELECT * FROM attacks 
            WHERE timestamp > ?
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (since, limit)).fetchall()
        conn.close()
        
        return [dict(row) for row in attacks]
    
    def get_attack_stats(self):
        """Get attack statistics"""
        conn = self.get_connection()
        
        stats = {}
        
        # Total attacks
        stats['total_attacks'] = conn.execute('SELECT COUNT(*) FROM attacks').fetchone()[0]
        
        # Attacks by service
        services = conn.execute('''
            SELECT service, COUNT(*) as count 
            FROM attacks 
            GROUP BY service 
            ORDER BY count DESC
        ''').fetchall()
        stats['by_service'] = [dict(row) for row in services]
        
        # Top attacking countries
        countries = conn.execute('''
            SELECT country, COUNT(*) as count 
            FROM attacks 
            WHERE country IS NOT NULL
            GROUP BY country 
            ORDER BY count DESC 
            LIMIT 10
        ''').fetchall()
        stats['top_countries'] = [dict(row) for row in countries]
        
        # Blocked IPs count
        stats['blocked_ips'] = conn.execute(
            'SELECT COUNT(*) FROM blocked_ips WHERE active = 1'
        ).fetchone()[0]
        
        conn.close()
        return stats
