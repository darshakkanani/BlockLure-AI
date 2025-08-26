from flask import Blueprint, jsonify, request
from models import Attack, Connection, BlockedIP
import sqlite3
from datetime import datetime, timedelta

api = Blueprint('api', __name__)

# Database helper
def get_db():
    conn = sqlite3.connect('../../data/attacks.db')
    conn.row_factory = sqlite3.Row
    return conn

@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@api.route('/dashboard-data', methods=['GET'])
def get_dashboard_data():
    """Get comprehensive dashboard data"""
    try:
        conn = get_db()
        
        # Recent attacks (last 24 hours)
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()
        recent_attacks = conn.execute('''
            SELECT service, COUNT(*) as count, MAX(timestamp) as last_attack
            FROM attacks 
            WHERE timestamp > ?
            GROUP BY service
            ORDER BY count DESC
        ''', (yesterday,)).fetchall()
        
        # Geographic distribution
        geo_data = conn.execute('''
            SELECT country, COUNT(*) as count
            FROM attacks 
            WHERE country IS NOT NULL AND timestamp > ?
            GROUP BY country
            ORDER BY count DESC
            LIMIT 10
        ''', (yesterday,)).fetchall()
        
        # Attack timeline (hourly for last 24h)
        timeline = conn.execute('''
            SELECT 
                strftime('%H:00', timestamp) as hour,
                COUNT(*) as attacks
            FROM attacks 
            WHERE timestamp > ?
            GROUP BY hour
            ORDER BY hour
        ''', (yesterday,)).fetchall()
        
        # Threat levels
        threat_levels = conn.execute('''
            SELECT 
                CASE 
                    WHEN threat_score >= 80 THEN 'Critical'
                    WHEN threat_score >= 60 THEN 'High'
                    WHEN threat_score >= 40 THEN 'Medium'
                    ELSE 'Low'
                END as level,
                COUNT(*) as count
            FROM attacks 
            WHERE timestamp > ?
            GROUP BY level
        ''', (yesterday,)).fetchall()
        
        conn.close()
        
        return jsonify({
            'recent_attacks': [dict(row) for row in recent_attacks],
            'geo_distribution': [dict(row) for row in geo_data],
            'timeline': [dict(row) for row in timeline],
            'threat_levels': [dict(row) for row in threat_levels]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/live-feed', methods=['GET'])
def get_live_feed():
    """Get live attack feed"""
    try:
        limit = int(request.args.get('limit', 20))
        
        conn = get_db()
        attacks = conn.execute('''
            SELECT * FROM attacks 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,)).fetchall()
        conn.close()
        
        return jsonify([dict(row) for row in attacks])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/threat-intel/<ip>', methods=['GET'])
def get_threat_intel(ip):
    """Get threat intelligence for specific IP"""
    try:
        conn = get_db()
        
        # Get all attacks from this IP
        attacks = conn.execute('''
            SELECT * FROM attacks 
            WHERE ip_address = ?
            ORDER BY timestamp DESC
        ''', (ip,)).fetchall()
        
        # Get block status
        blocked = conn.execute('''
            SELECT * FROM blocked_ips 
            WHERE ip_address = ? AND active = 1
        ''', (ip,)).fetchone()
        
        conn.close()
        
        return jsonify({
            'ip_address': ip,
            'attack_history': [dict(row) for row in attacks],
            'blocked': dict(blocked) if blocked else None,
            'total_attacks': len(attacks)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
