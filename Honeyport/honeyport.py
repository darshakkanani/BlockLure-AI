import socket, threading, time, json, os, re, signal, sys, hashlib
import requests
from datetime import datetime
from collections import defaultdict, deque

# ----------------------------
# CONFIG - ENHANCED FOR WIDE AREA NETWORK EXPOSURE
# ----------------------------
import netifaces

# Get the actual external IP interface (not localhost)
def get_external_ip():
    """Get the actual external IP address for cellular/mobile networks"""
    try:
        # Get all network interfaces
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            if interface.startswith(('en', 'wlan', 'eth', 'ppp')):  # Common external interfaces
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        ip = addr['addr']
                        # Skip localhost and link-local addresses
                        if not ip.startswith(('127.', '169.254.', '0.')):
                            return ip
    except:
        pass
    return "0.0.0.0"  # Fallback to bind all interfaces

HOST = get_external_ip()
print(f"[*] Binding to external IP: {HOST}")

# Use standard ports that attract more attackers and are commonly scanned
PORTS = {
    22: "banners/ssh.txt",        # Standard SSH port - highly targeted
    23: "banners/telnet.txt",     # Standard Telnet port - legacy systems
    80: "fake_http.html",         # Standard HTTP port - most scanned
    443: "fake_http.html",        # HTTPS port - second most scanned  
    21: "banners/ftp.txt",        # FTP port - file transfer attacks
    25: "banners/smtp.txt",       # SMTP port - email server attacks
    53: "banners/dns.txt",        # DNS port - infrastructure attacks
    110: "banners/pop3.txt",      # POP3 port - email attacks
    143: "banners/imap.txt",      # IMAP port - email attacks
    3306: "banners/mysql.txt",    # MySQL port - database attacks
    5432: "banners/postgres.txt", # PostgreSQL port - database attacks
    1433: "banners/mssql.txt",    # MSSQL port - database attacks
    3389: "banners/rdp.txt",      # RDP port - remote desktop attacks
    445: "banners/smb.txt",       # SMB port - Windows file sharing
    135: "banners/rpc.txt",       # RPC port - Windows services
    139: "banners/netbios.txt",   # NetBIOS port - Windows networking
}
LOG_FILE = "honeyport.log"

# Global tracking for attack patterns
attack_tracker = defaultdict(lambda: {
    'connections': deque(maxlen=100),
    'total_attempts': 0,
    'first_seen': None,
    'last_seen': None,
    'ports_scanned': set(),
    'tools_detected': set(),
    'credentials_tried': [],
    'exploit_attempts': []
})

# ----------------------------
# Load response data
# ----------------------------
def load_file(path):
    if not os.path.exists(path):
        return b""
    with open(path, "rb") as f:
        return f.read()

RESPONSES = {port: load_file(path) for port, path in PORTS.items()}

# For HTTP port, wrap file in HTTP headers
if 8080 in RESPONSES:
    html = RESPONSES[8080]
    http_resp = (b"HTTP/1.1 200 OK\r\n"
                 b"Server: Apache/2.4.41 (Ubuntu)\r\n"
                 b"Content-Type: text/html\r\nConnection: close\r\n"
                 + f"Content-Length: {len(html)}\r\n\r\n".encode() + html)
    RESPONSES[8080] = http_resp

# ----------------------------
# Enhanced Analysis Functions
# ----------------------------
def get_geolocation(ip):
    """Get comprehensive geolocation data for attacker identification"""
    if ip == "127.0.0.1" or ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("172."):
        return {
            "country": "Local Network",
            "city": "Local",
            "region": "Local",
            "isp": "Local Network",
            "asn": "Local",
            "timezone": "Local",
            "lat": 0,
            "lon": 0,
            "threat_level": "LOW"
        }
    
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "country": data.get("country", "Unknown"),
                "country_code": data.get("countryCode", "Unknown"),
                "city": data.get("city", "Unknown"),
                "region": data.get("regionName", "Unknown"),
                "isp": data.get("isp", "Unknown"),
                "organization": data.get("org", "Unknown"),
                "asn": data.get("as", "Unknown"),
                "timezone": data.get("timezone", "Unknown"),
                "lat": data.get("lat", 0),
                "lon": data.get("lon", 0),
                "zip_code": data.get("zip", "Unknown"),
                "threat_level": "HIGH" if data.get("country") in ["Russia", "China", "North Korea"] else "MEDIUM"
            }
    except Exception as e:
        pass
    return {"country": "Unknown", "city": "Unknown", "region": "Unknown", "isp": "Unknown", "threat_level": "UNKNOWN"}

def detect_attack_tools(request_data):
    """Detect specific attack tools and signatures"""
    request_str = request_data.decode(errors="ignore")
    tools_detected = []
    
    # Tool signatures in User-Agent or request
    tool_signatures = {
        'nmap': ['nmap', 'nmaplowercheck', 'nmapuppercheck'],
        'sqlmap': ['sqlmap', 'User-Agent: sqlmap'],
        'hydra': ['hydra', 'THC-Hydra'],
        'medusa': ['medusa'],
        'metasploit': ['metasploit', 'meterpreter', 'msf'],
        'nikto': ['nikto'],
        'dirb': ['dirb'],
        'gobuster': ['gobuster'],
        'burp': ['burp suite', 'burp'],
        'zap': ['zap', 'zaproxy'],
        'masscan': ['masscan'],
        'curl': ['curl/'],
        'wget': ['wget/'],
        'python-requests': ['python-requests', 'requests/'],
        'shodan': ['shodan'],
        'censys': ['censys']
    }
    
    for tool, signatures in tool_signatures.items():
        if any(sig in request_str.lower() for sig in signatures):
            tools_detected.append(tool.upper())
    
    return tools_detected

def analyze_reconnaissance_data(request_data, port):
    """Analyze reconnaissance attempts and banner grabbing"""
    request_str = request_data.decode(errors="ignore")
    recon_data = {
        'banner_grab_attempt': False,
        'version_detection': False,
        'service_enumeration': False,
        'vulnerability_scan': False
    }
    
    # Banner grabbing detection
    if port == 2222 and 'SSH-' in request_str:
        recon_data['banner_grab_attempt'] = True
        recon_data['version_detection'] = True
    
    # Service enumeration
    common_paths = ['/robots.txt', '/.well-known/', '/sitemap.xml', '/admin', '/login']
    if any(path in request_str for path in common_paths):
        recon_data['service_enumeration'] = True
    
    # Vulnerability scanning
    vuln_indicators = ['/.env', '/config', '/backup', '/.git', '/wp-admin', '/phpmyadmin']
    if any(indicator in request_str for indicator in vuln_indicators):
        recon_data['vulnerability_scan'] = True
    
    return recon_data

def extract_exploit_attempts(request_data, port):
    """Extract and analyze potential exploit attempts"""
    request_str = request_data.decode(errors="ignore")
    exploits = []
    
    # SQL Injection patterns
    sql_patterns = [
        "' or 1=1", "' or '1'='1", "union select", "drop table", 
        "insert into", "delete from", "' or 1=1 --", "admin'--"
    ]
    for pattern in sql_patterns:
        if pattern in request_str.lower():
            exploits.append({
                'type': 'SQL_INJECTION',
                'pattern': pattern,
                'payload': request_str[:200]
            })
    
    # Command injection
    cmd_patterns = [';cat /etc/passwd', ';id', '`whoami`', '$(whoami)', '|nc ', ';wget ', ';curl ']
    for pattern in cmd_patterns:
        if pattern in request_str.lower():
            exploits.append({
                'type': 'COMMAND_INJECTION',
                'pattern': pattern,
                'payload': request_str[:200]
            })
    
    # XSS patterns
    xss_patterns = ['<script>', 'javascript:', 'onerror=', 'onload=', 'alert(', 'document.cookie']
    for pattern in xss_patterns:
        if pattern in request_str.lower():
            exploits.append({
                'type': 'XSS',
                'pattern': pattern,
                'payload': request_str[:200]
            })
    
    # Default credentials
    default_creds = [
        'admin:admin', 'root:root', 'admin:password', 'root:toor',
        'admin:123456', 'user:user', 'guest:guest', 'test:test'
    ]
    for cred in default_creds:
        if cred in request_str.lower():
            exploits.append({
                'type': 'DEFAULT_CREDENTIALS',
                'pattern': cred,
                'payload': request_str[:200]
            })
    
    return exploits

def analyze_attack_patterns(request_data, port, source_ip):
    """Comprehensive attack pattern analysis"""
    patterns = []
    methodology = []
    request_str = request_data.decode(errors="ignore").lower()
    
    # Tool detection
    tools = detect_attack_tools(request_data)
    if tools:
        patterns.extend([f"TOOL_{tool}" for tool in tools])
        methodology.extend([f"Automated scanning with {tool.lower()}" for tool in tools])
    
    # Reconnaissance analysis
    recon = analyze_reconnaissance_data(request_data, port)
    if recon['banner_grab_attempt']:
        patterns.append("BANNER_GRABBING")
        methodology.append("Service banner enumeration")
    if recon['vulnerability_scan']:
        patterns.append("VULNERABILITY_SCAN")
        methodology.append("Automated vulnerability scanning")
    
    # Exploit attempts
    exploits = extract_exploit_attempts(request_data, port)
    for exploit in exploits:
        patterns.append(exploit['type'])
        methodology.append(f"{exploit['type'].replace('_', ' ').title()} attempt")
    
    # Port-specific analysis for standard ports
    if port == 22:  # SSH
        if 'ssh-' in request_str:
            patterns.append("SSH_PROBE")
            methodology.append("SSH service probing")
    elif port == 23:  # Telnet
        if len(request_data) > 0:
            patterns.append("TELNET_LOGIN_ATTEMPT")
            methodology.append("Telnet login brute force")
    elif port in [80, 443]:  # HTTP/HTTPS
        if 'get /' in request_str or 'post /' in request_str:
            patterns.append("WEB_PROBE")
            methodology.append("Web application probing")
    elif port == 21:  # FTP
        patterns.append("FTP_PROBE")
        methodology.append("FTP file transfer probing")
    elif port == 25:  # SMTP
        patterns.append("SMTP_PROBE")
        methodology.append("Email server enumeration")
    elif port == 53:  # DNS
        patterns.append("DNS_PROBE")
        methodology.append("DNS infrastructure probing")
    elif port in [110, 143]:  # POP3/IMAP
        patterns.append("EMAIL_PROBE")
        methodology.append("Email service enumeration")
    elif port in [3306, 5432, 1433]:  # Database ports
        patterns.append("DATABASE_PROBE")
        methodology.append("Database connection attempt")
    elif port == 3389:  # RDP
        patterns.append("RDP_PROBE")
        methodology.append("Remote desktop connection attempt")
    elif port in [445, 135, 139]:  # Windows services
        patterns.append("WINDOWS_PROBE")
        methodology.append("Windows service enumeration")
    
    return patterns, methodology, exploits

def extract_credentials(request_data):
    """Extract credentials from various protocols and formats"""
    credentials = {}
    try:
        request_str = request_data.decode(errors="ignore")
        
        # HTTP form data
        if "=" in request_str and "&" in request_str:
            pairs = request_str.split("&")
            for pair in pairs:
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    if key.lower() in ['user', 'username', 'userid', 'login', 'u']:
                        credentials['username'] = value
                    elif key.lower() in ['pass', 'password', 'pwd', 'p']:
                        credentials['password'] = value
        
        # Basic Auth (HTTP)
        if 'authorization: basic' in request_str.lower():
            auth_line = [line for line in request_str.split('\n') if 'authorization: basic' in line.lower()]
            if auth_line:
                credentials['auth_type'] = 'Basic Authentication'
                credentials['encoded_creds'] = auth_line[0].split('Basic ')[1].strip()
        
        # SSH login attempts
        if 'ssh-' in request_str.lower():
            credentials['protocol'] = 'SSH'
            credentials['client_version'] = request_str.strip()
        
        # Telnet login attempts (look for common patterns)
        telnet_patterns = ['login:', 'password:', 'username:']
        if any(pattern in request_str.lower() for pattern in telnet_patterns):
            credentials['protocol'] = 'Telnet'
            credentials['login_attempt'] = request_str.strip()
            
    except:
        pass
    return credentials

def update_attack_tracker(ip, port, patterns, credentials, exploits):
    """Update global attack tracking for pattern analysis"""
    current_time = time.time()
    tracker = attack_tracker[ip]
    
    # Update connection tracking
    tracker['connections'].append({
        'timestamp': current_time,
        'port': port,
        'patterns': patterns
    })
    tracker['total_attempts'] += 1
    tracker['ports_scanned'].add(port)
    
    if tracker['first_seen'] is None:
        tracker['first_seen'] = current_time
    tracker['last_seen'] = current_time
    
    # Track tools
    for pattern in patterns:
        if pattern.startswith('TOOL_'):
            tracker['tools_detected'].add(pattern)
    
    # Track credentials
    if credentials:
        tracker['credentials_tried'].append({
            'timestamp': current_time,
            'port': port,
            'credentials': credentials
        })
    
    # Track exploits
    if exploits:
        tracker['exploit_attempts'].extend(exploits)
    
    return tracker

def calculate_attack_frequency(tracker):
    """Calculate attack frequency and timing patterns"""
    connections = list(tracker['connections'])
    if len(connections) < 2:
        return {'frequency': 'Single attempt', 'pattern': 'Isolated'}
    
    # Calculate time differences
    time_diffs = []
    for i in range(1, len(connections)):
        diff = connections[i]['timestamp'] - connections[i-1]['timestamp']
        time_diffs.append(diff)
    
    avg_interval = sum(time_diffs) / len(time_diffs)
    
    if avg_interval < 5:
        return {'frequency': 'Very High (< 5s intervals)', 'pattern': 'Automated/Bot'}
    elif avg_interval < 30:
        return {'frequency': 'High (< 30s intervals)', 'pattern': 'Scripted'}
    elif avg_interval < 300:
        return {'frequency': 'Medium (< 5min intervals)', 'pattern': 'Semi-automated'}
    else:
        return {'frequency': 'Low (> 5min intervals)', 'pattern': 'Manual'}

# ----------------------------
# Enhanced Logger with COMPLETE Attacker Intelligence
# ----------------------------
def log_event(ip, port, request_data, source_port=None):
    """Log comprehensive attacker intelligence as requested"""
    
    # 1. ATTACKER IDENTIFICATION
    geo_info = get_geolocation(ip)
    
    # 2. ATTACK PATTERNS & RECONNAISSANCE
    attack_patterns, methodology, exploits = analyze_attack_patterns(request_data, port, ip)
    
    # 3. CREDENTIALS & PAYLOADS
    credentials = extract_credentials(request_data)
    
    # 4. ATTACK TOOLS & SIGNATURES
    tools_detected = detect_attack_tools(request_data)
    
    # 5. UPDATE ATTACK TRACKING
    tracker = update_attack_tracker(ip, port, attack_patterns, credentials, exploits)
    frequency_analysis = calculate_attack_frequency(tracker)
    
    # 6. PROTOCOL ANALYSIS
    protocol_map = {2222: "SSH", 2323: "Telnet", 4445: "SMB", 3306: "MySQL", 8080: "HTTP"}
    protocol = protocol_map.get(port, "Unknown")
    
    # 7. COMPREHENSIVE EVENT LOG
    event = {
        "timestamp": datetime.now().isoformat(),
        "unix_timestamp": time.time(),
        
        # ATTACKER IDENTIFICATION
        "attacker_identification": {
            "source_ip": ip,
            "source_port": source_port,
            "geolocation": geo_info,
            "first_seen": datetime.fromtimestamp(tracker['first_seen']).isoformat() if tracker['first_seen'] else None,
            "last_seen": datetime.fromtimestamp(tracker['last_seen']).isoformat() if tracker['last_seen'] else None,
            "total_attempts": tracker['total_attempts']
        },
        
        # CONNECTION INFO
        "connection_info": {
            "target_port": port,
            "protocol": protocol,
            "connection_duration": "N/A",
            "bytes_transferred": len(request_data)
        },
        
        # ATTACK PATTERNS
        "attack_patterns": {
            "detected_patterns": attack_patterns,
            "attack_methodology": methodology,
            "frequency_analysis": frequency_analysis,
            "ports_scanned": list(tracker['ports_scanned']),
            "scan_duration": tracker['last_seen'] - tracker['first_seen'] if tracker['first_seen'] and tracker['last_seen'] else 0
        },
        
        # RECONNAISSANCE DATA
        "reconnaissance": {
            "banner_grabbing": "SSH-" in request_data.decode(errors="ignore") if port == 2222 else False,
            "service_enumeration": any(path in request_data.decode(errors="ignore").lower() for path in ['/admin', '/login', '/config']),
            "vulnerability_scanning": any(vuln in request_data.decode(errors="ignore").lower() for vuln in ['/.env', '/wp-admin', '/phpmyadmin']),
            "port_scanning": len(tracker['ports_scanned']) > 1
        },
        
        # ATTACK TOOLS & SIGNATURES
        "attack_tools": {
            "detected_tools": tools_detected,
            "all_tools_seen": list(tracker['tools_detected']),
            "automation_indicators": {
                "is_automated": len(tools_detected) > 0 or frequency_analysis['pattern'] in ['Automated/Bot', 'Scripted'],
                "bot_signatures": [tool for tool in tools_detected if tool in ['NMAP', 'MASSCAN', 'SHODAN']],
                "user_agent": _extract_user_agent(request_data)
            }
        },
        
        # PAYLOADS & REQUESTS
        "payload_analysis": {
            "raw_payload": request_data.decode(errors="ignore")[:500],  # First 500 chars
            "payload_size": len(request_data),
            "payload_hash": hashlib.md5(request_data).hexdigest(),
            "protocol_specific_data": _analyze_protocol_data(request_data, port),
            "http_headers": _extract_http_headers(request_data) if port == 8080 else None
        },
        
        # CREDENTIALS & AUTHENTICATION
        "credentials_analysis": {
            "extracted_credentials": credentials,
            "all_credentials_tried": tracker['credentials_tried'][-10:],  # Last 10 attempts
            "brute_force_indicators": {
                "multiple_attempts": len(tracker['credentials_tried']) > 1,
                "common_passwords": _detect_common_passwords(tracker['credentials_tried']),
                "credential_stuffing": len(set(cred.get('credentials', {}).get('username', '') for cred in tracker['credentials_tried'])) > 3
            }
        },
        
        # EXPLOIT ATTEMPTS
        "exploit_analysis": {
            "current_exploits": exploits,
            "all_exploit_attempts": tracker['exploit_attempts'][-5:],  # Last 5 exploits
            "exploit_categories": list(set(exploit['type'] for exploit in tracker['exploit_attempts'])),
            "dangerous_payloads": [exploit for exploit in exploits if exploit['type'] in ['COMMAND_INJECTION', 'SQL_INJECTION']]
        },
        
        # THREAT ASSESSMENT
        "threat_assessment": {
            "threat_level": _calculate_threat_level(attack_patterns, geo_info, tracker),
            "risk_score": _calculate_risk_score(tracker, exploits, geo_info),
            "persistence_score": min(tracker['total_attempts'] * 10, 100),
            "sophistication_level": _assess_sophistication(tools_detected, exploits, frequency_analysis)
        }
    }
    
    # Write to log file
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event, indent=2) + "\n")
    
    # Enhanced console output
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🚨 ATTACK DETECTED")
    print(f"    📍 SOURCE: {ip}:{source_port or 'Unknown'} -> {port} ({protocol})")
    print(f"    🌍 LOCATION: {geo_info.get('city', 'Unknown')}, {geo_info.get('country', 'Unknown')} ({geo_info.get('isp', 'Unknown')})")
    
    if attack_patterns:
        print(f"    ⚔️  ATTACK PATTERNS: {', '.join(attack_patterns)}")
    if tools_detected:
        print(f"    🔧 TOOLS: {', '.join(tools_detected)}")
    if credentials:
        print(f"    🔑 CREDENTIALS: {credentials}")
    if exploits:
        print(f"    💥 EXPLOITS: {len(exploits)} detected")
    
    print(f"    📊 FREQUENCY: {frequency_analysis['frequency']} ({frequency_analysis['pattern']})")
    print(f"    🎯 TOTAL ATTEMPTS: {tracker['total_attempts']} | PORTS: {len(tracker['ports_scanned'])}")

def _extract_user_agent(request_data):
    """Extract User-Agent from HTTP requests"""
    try:
        request_str = request_data.decode(errors="ignore")
        for line in request_str.split('\n'):
            if line.lower().startswith('user-agent:'):
                return line.split(':', 1)[1].strip()
    except:
        pass
    return "Unknown"

def _extract_http_headers(request_data):
    """Extract HTTP headers for analysis"""
    headers = {}
    try:
        request_str = request_data.decode(errors="ignore")
        lines = request_str.split('\n')
        for line in lines[1:]:  # Skip request line
            if ':' in line and line.strip():
                key, value = line.split(':', 1)
                headers[key.strip().lower()] = value.strip()
    except:
        pass
    return headers

def _analyze_protocol_data(request_data, port):
    """Analyze protocol-specific data"""
    request_str = request_data.decode(errors="ignore")
    
    if port == 2222:  # SSH
        return {"ssh_version": request_str.strip() if "SSH-" in request_str else None}
    elif port == 2323:  # Telnet
        return {"telnet_data": request_str.strip()[:100]}
    elif port == 3306:  # MySQL
        return {"mysql_probe": len(request_data) > 0}
    elif port == 4445:  # SMB
        return {"smb_probe": True}
    elif port == 8080:  # HTTP
        return {
            "http_method": request_str.split()[0] if request_str.split() else "Unknown",
            "http_path": request_str.split()[1] if len(request_str.split()) > 1 else "/",
            "http_version": request_str.split()[2] if len(request_str.split()) > 2 else "Unknown"
        }
    return {}

def _detect_common_passwords(credentials_list):
    """Detect common passwords in brute force attempts"""
    common_passwords = ['123456', 'password', 'admin', 'root', '12345', 'qwerty', 'letmein']
    found_common = []
    
    for cred_attempt in credentials_list:
        password = cred_attempt.get('credentials', {}).get('password', '')
        if password.lower() in common_passwords:
            found_common.append(password)
    
    return list(set(found_common))

def _calculate_threat_level(patterns, geo_info, tracker):
    """Calculate comprehensive threat level"""
    score = 0
    
    # Pattern-based scoring
    high_risk_patterns = ['SQL_INJECTION', 'COMMAND_INJECTION', 'TOOL_SQLMAP', 'TOOL_METASPLOIT']
    score += sum(10 for pattern in patterns if pattern in high_risk_patterns)
    score += len(patterns) * 2
    
    # Geographic risk
    if geo_info.get('threat_level') == 'HIGH':
        score += 20
    elif geo_info.get('threat_level') == 'MEDIUM':
        score += 10
    
    # Persistence scoring
    score += min(tracker['total_attempts'] * 2, 30)
    score += len(tracker['ports_scanned']) * 5
    
    if score >= 50:
        return "CRITICAL"
    elif score >= 30:
        return "HIGH"
    elif score >= 15:
        return "MEDIUM"
    else:
        return "LOW"

def _calculate_risk_score(tracker, exploits, geo_info):
    """Calculate numerical risk score (0-100)"""
    score = 0
    score += min(tracker['total_attempts'] * 3, 30)
    score += len(tracker['ports_scanned']) * 5
    score += len(exploits) * 10
    score += len(tracker['tools_detected']) * 8
    
    if geo_info.get('threat_level') == 'HIGH':
        score += 25
    
    return min(score, 100)

def _assess_sophistication(tools, exploits, frequency):
    """Assess attacker sophistication level"""
    if any(tool in ['METASPLOIT', 'SQLMAP'] for tool in tools):
        return "Advanced"
    elif len(tools) > 2 or len(exploits) > 3:
        return "Intermediate"
    elif frequency['pattern'] == 'Automated/Bot':
        return "Script Kiddie"
    else:
        return "Basic"

# ----------------------------
# Handler per connection
# ----------------------------
def handle_client(conn, addr, port):
    ip, prt = addr
    conn.settimeout(5)
    req_data = b""
    try:
        req_data = conn.recv(4096)
        if port in RESPONSES:
            conn.sendall(RESPONSES[port])
    except Exception:
        pass
    finally:
        conn.close()

    # Enhanced logging
    log_event(ip, port, req_data, prt)

# ----------------------------
# Start listener for each port
# ----------------------------
def start_listener(port):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, port))
    s.listen(50)
    print(f"[+] Listening on {HOST}:{port}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr, port), daemon=True).start()

# ----------------------------
# Signal handlers for graceful shutdown
# ----------------------------
def signal_handler(sig, frame):
    print(f"\n[!] Received signal {sig}, shutting down gracefully...")
    print("[*] Honeyport stopped")
    sys.exit(0)

# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("=" * 60)
    print("🍯 ADVANCED MULTI-PROTOCOL HONEYPORT SYSTEM")
    print("=" * 60)
    print(f"📡 Host: {HOST}")
    print(f"📝 Log File: {LOG_FILE}")
    print("🔍 Protocols:")
    for port, banner_file in PORTS.items():
        protocol_map = {2222: "SSH", 2323: "Telnet", 4445: "SMB", 3306: "MySQL", 8081: "HTTP"}
        protocol = protocol_map.get(port, "Unknown")
        print(f"   • {protocol} on port {port}")
    print("=" * 60)
    
    # Start listeners
    for port in PORTS:
        try:
            threading.Thread(target=start_listener, args=(port,), daemon=True).start()
        except Exception as e:
            print(f"[-] Failed to start listener on port {port}: {e}")
    
    print("[*] All listeners started. Waiting for connections...")
    print("[*] Press Ctrl+C to stop")
    
    # Keep running
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
