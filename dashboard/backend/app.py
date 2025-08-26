from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

# Database path
DB_PATH = "../../data/attacks.db"

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    try:
        conn = get_db_connection()
        
        # Total attacks
        total_attacks = conn.execute('SELECT COUNT(*) FROM attacks').fetchone()[0]
        
        # Attacks in last 24 hours
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()
        recent_attacks = conn.execute(
            'SELECT COUNT(*) FROM attacks WHERE timestamp > ?', 
            (yesterday,)
        ).fetchone()[0]
        
        # Unique IPs
        unique_ips = conn.execute('SELECT COUNT(DISTINCT ip_address) FROM attacks').fetchone()[0]
        
        # Blocked IPs
        blocked_ips = conn.execute('SELECT COUNT(*) FROM blocked_ips WHERE active = 1').fetchone()[0]
        
        # Top services attacked
        services = conn.execute('''
            SELECT service, COUNT(*) as count 
            FROM attacks 
            GROUP BY service 
            ORDER BY count DESC 
            LIMIT 5
        ''').fetchall()
        
        conn.close()
        
        return jsonify({
            'total_attacks': total_attacks,
            'recent_attacks': recent_attacks,
            'unique_ips': unique_ips,
            'blocked_ips': blocked_ips,
            'top_services': [dict(row) for row in services]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attacks', methods=['GET'])
def get_attacks():
    """Get recent attacks with pagination"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        offset = (page - 1) * limit
        
        conn = get_db_connection()
        
        attacks = conn.execute('''
            SELECT * FROM attacks 
            ORDER BY timestamp DESC 
            LIMIT ? OFFSET ?
        ''', (limit, offset)).fetchall()
        
        total = conn.execute('SELECT COUNT(*) FROM attacks').fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'attacks': [dict(row) for row in attacks],
            'total': total,
            'page': page,
            'limit': limit
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attacks/geo', methods=['GET'])
def get_geo_attacks():
    """Get attacks with geolocation data for map visualization"""
    try:
        hours = int(request.args.get('hours', 24))
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        conn = get_db_connection()
        
        attacks = conn.execute('''
            SELECT ip_address, country, city, latitude, longitude, 
                   COUNT(*) as attack_count, MAX(timestamp) as last_attack
            FROM attacks 
            WHERE timestamp > ? AND latitude IS NOT NULL AND longitude IS NOT NULL
            GROUP BY ip_address, country, city, latitude, longitude
            ORDER BY attack_count DESC
        ''', (since,)).fetchall()
        
        conn.close()
        
        return jsonify([dict(row) for row in attacks])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attacks/timeline', methods=['GET'])
def get_attack_timeline():
    """Get attack timeline data"""
    try:
        hours = int(request.args.get('hours', 24))
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        conn = get_db_connection()
        
        # Group attacks by hour
        timeline = conn.execute('''
            SELECT 
                strftime('%Y-%m-%d %H:00:00', timestamp) as hour,
                service,
                COUNT(*) as count
            FROM attacks 
            WHERE timestamp > ?
            GROUP BY hour, service
            ORDER BY hour
        ''', (since,)).fetchall()
        
        conn.close()
        
        return jsonify([dict(row) for row in timeline])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/top-attackers', methods=['GET'])
def get_top_attackers():
    """Get top attacking IPs"""
    try:
        limit = int(request.args.get('limit', 10))
        hours = int(request.args.get('hours', 24))
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        conn = get_db_connection()
        
        attackers = conn.execute('''
            SELECT 
                ip_address,
                country,
                city,
                COUNT(*) as attack_count,
                MAX(timestamp) as last_attack,
                GROUP_CONCAT(DISTINCT service) as services
            FROM attacks 
            WHERE timestamp > ?
            GROUP BY ip_address
            ORDER BY attack_count DESC
            LIMIT ?
        ''', (since, limit)).fetchall()
        
        conn.close()
        
        return jsonify([dict(row) for row in attackers])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blocked-ips', methods=['GET'])
def get_blocked_ips():
    """Get currently blocked IPs"""
    try:
        conn = get_db_connection()
        
        blocked = conn.execute('''
            SELECT * FROM blocked_ips 
            WHERE active = 1 
            ORDER BY blocked_at DESC
        ''').fetchall()
        
        conn.close()
        
        return jsonify([dict(row) for row in blocked])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/block-ip', methods=['POST'])
def block_ip():
    """Manually block an IP address"""
    try:
        data = request.get_json()
        ip_address = data.get('ip_address')
        reason = data.get('reason', 'Manual block')
        
        if not ip_address:
            return jsonify({'error': 'IP address required'}), 400
        
        conn = get_db_connection()
        
        # Add to blocked IPs table
        conn.execute('''
            INSERT OR REPLACE INTO blocked_ips 
            (ip_address, blocked_at, reason, expires_at, active)
            VALUES (?, ?, ?, ?, 1)
        ''', (
            ip_address,
            datetime.now().isoformat(),
            reason,
            (datetime.now() + timedelta(hours=24)).isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': f'IP {ip_address} blocked'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/unblock-ip', methods=['POST'])
def unblock_ip():
    """Manually unblock an IP address"""
    try:
        data = request.get_json()
        ip_address = data.get('ip_address')
        
        if not ip_address:
            return jsonify({'error': 'IP address required'}), 400
        
        conn = get_db_connection()
        
        # Mark as inactive
        conn.execute('''
            UPDATE blocked_ips 
            SET active = 0 
            WHERE ip_address = ?
        ''', (ip_address,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': f'IP {ip_address} unblocked'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search_attacks():
    """Search attacks by IP, service, or other criteria"""
    try:
        query = request.args.get('q', '')
        service = request.args.get('service', '')
        country = request.args.get('country', '')
        limit = int(request.args.get('limit', 50))
        
        conn = get_db_connection()
        
        sql = 'SELECT * FROM attacks WHERE 1=1'
        params = []
        
        if query:
            sql += ' AND (ip_address LIKE ? OR details LIKE ?)'
            params.extend([f'%{query}%', f'%{query}%'])
        
        if service:
            sql += ' AND service = ?'
            params.append(service)
        
        if country:
            sql += ' AND country = ?'
            params.append(country)
        
        sql += ' ORDER BY timestamp DESC LIMIT ?'
        params.append(limit)
        
        results = conn.execute(sql, params).fetchall()
        conn.close()
        
        return jsonify([dict(row) for row in results])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export', methods=['GET'])
def export_data():
    """Export attack data as JSON"""
    try:
        format_type = request.args.get('format', 'json')
        hours = int(request.args.get('hours', 24))
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        conn = get_db_connection()
        
        attacks = conn.execute('''
            SELECT * FROM attacks 
            WHERE timestamp > ?
            ORDER BY timestamp DESC
        ''', (since,)).fetchall()
        
        conn.close()
        
        data = [dict(row) for row in attacks]
        
        if format_type == 'json':
            return jsonify(data)
        else:
            return jsonify({'error': 'Only JSON format supported'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure database directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
