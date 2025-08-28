#!/usr/bin/env python3
"""
Cellular Network Honeyport - Designed for mobile/cellular connections
Combines multiple exposure methods to ensure attackers can reach your honeyport
"""

import socket, threading, time, json, os, re, signal, sys, hashlib
import requests, subprocess
from datetime import datetime
from collections import defaultdict, deque

# ----------------------------
# CELLULAR NETWORK CONFIGURATION
# ----------------------------

# Use localhost since cellular networks block direct external access
HOST = "127.0.0.1"
print(f"[*] Cellular network detected - using tunneling approach")

# Standard ports that attract attackers
PORTS = {
    2222: "banners/ssh.txt",      # SSH (non-privileged)
    2323: "banners/telnet.txt",   # Telnet (non-privileged)
    8080: "fake_http.html",       # HTTP (non-privileged)
    8443: "fake_http.html",       # HTTPS (non-privileged)
    2121: "banners/ftp.txt",      # FTP (non-privileged)
    2525: "banners/smtp.txt",     # SMTP (non-privileged)
    3306: "banners/mysql.txt",    # MySQL
    5432: "banners/postgres.txt", # PostgreSQL
    1433: "banners/mssql.txt",    # MSSQL
    3389: "banners/rdp.txt",      # RDP
    4445: "banners/smb.txt",      # SMB (non-privileged)
    1135: "banners/rpc.txt",      # RPC (non-privileged)
    1139: "banners/netbios.txt",  # NetBIOS (non-privileged)
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
# NGROK TUNNEL MANAGER
# ----------------------------
class TunnelManager:
    def __init__(self):
        self.tunnels = {}
        self.tunnel_urls = {}
        
    def start_all_tunnels(self):
        """Start ngrok tunnels for all ports"""
        print("\n🚀 STARTING CELLULAR HONEYPORT TUNNELS")
        print("=" * 50)
        
        # Kill existing ngrok processes
        subprocess.run(["pkill", "-f", "ngrok"], capture_output=True)
        time.sleep(2)
        
        tunnel_commands = []
        for port in PORTS.keys():
            if port == 8080:  # HTTP tunnel
                cmd = f"ngrok http {port} --log=stdout > /tmp/ngrok_http_{port}.log 2>&1 &"
            else:  # TCP tunnels
                cmd = f"ngrok tcp {port} --log=stdout > /tmp/ngrok_tcp_{port}.log 2>&1 &"
            
            tunnel_commands.append((port, cmd))
        
        # Start all tunnels
        for port, cmd in tunnel_commands:
            os.system(cmd)
            print(f"📡 Starting tunnel for port {port}")
        
        print("\n⏳ Waiting for tunnels to initialize...")
        time.sleep(8)
        
        # Extract tunnel URLs
        self.extract_tunnel_urls()
        
    def extract_tunnel_urls(self):
        """Extract public URLs from ngrok logs"""
        print("\n🌐 ACTIVE TUNNEL URLS:")
        print("=" * 30)
        
        for port in PORTS.keys():
            if port == 8080:
                log_file = f"/tmp/ngrok_http_{port}.log"
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        content = f.read()
                        # Extract HTTPS URL
                        https_match = re.search(r'https://[^\s]+\.ngrok-free\.app', content)
                        if https_match:
                            url = https_match.group()
                            self.tunnel_urls[port] = url
                            print(f"🌐 HTTP (port {port}):  {url}")
            else:
                log_file = f"/tmp/ngrok_tcp_{port}.log"
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        content = f.read()
                        # Extract TCP URL
                        tcp_match = re.search(r'tcp://[^\s]+', content)
                        if tcp_match:
                            url = tcp_match.group()
                            self.tunnel_urls[port] = url
                            service_name = self.get_service_name(port)
                            print(f"🔐 {service_name} (port {port}): {url}")
        
        print(f"\n🎯 TOTAL ACTIVE TUNNELS: {len(self.tunnel_urls)}")
        
    def get_service_name(self, port):
        """Get service name for port"""
        service_map = {
            2222: "SSH", 2323: "Telnet", 3306: "MySQL", 5432: "PostgreSQL",
            1433: "MSSQL", 3389: "RDP", 4445: "SMB", 2121: "FTP",
            2525: "SMTP", 1135: "RPC", 1139: "NetBIOS"
        }
        return service_map.get(port, "Unknown")
    
    def save_tunnel_info(self):
        """Save tunnel information for attackers to find"""
        tunnel_info = {
            "timestamp": datetime.now().isoformat(),
            "cellular_network": True,
            "public_tunnels": self.tunnel_urls,
            "attack_surfaces": list(PORTS.keys()),
            "discovery_methods": [
                "ngrok tunnel scanning",
                "subdomain enumeration", 
                "tunnel URL discovery",
                "automated security scans"
            ],
            "target_services": {
                "ssh": [url for port, url in self.tunnel_urls.items() if port == 2222],
                "web": [url for port, url in self.tunnel_urls.items() if port == 8080],
                "database": [url for port, url in self.tunnel_urls.items() if port in [3306, 5432, 1433]],
                "windows": [url for port, url in self.tunnel_urls.items() if port in [3389, 4445, 1135, 1139]]
            }
        }
        
        with open("cellular_exposure.json", "w") as f:
            json.dump(tunnel_info, f, indent=2)
        
        print(f"[*] Tunnel information saved to cellular_exposure.json")

# ----------------------------
# Load response data (same as original)
# ----------------------------
def load_file(path):
    if not os.path.exists(path):
        return b""
    with open(path, "rb") as f:
        return f.read()

RESPONSES = {port: load_file(path) for port, path in PORTS.items()}

# For HTTP ports, wrap in HTTP headers
for port in [8080, 8443]:
    if port in RESPONSES:
        html = RESPONSES[port]
        http_resp = (b"HTTP/1.1 200 OK\r\n"
                     b"Server: Apache/2.4.41 (Ubuntu)\r\n"
                     b"Content-Type: text/html\r\nConnection: close\r\n"
                     + f"Content-Length: {len(html)}\r\n\r\n".encode() + html)
        RESPONSES[port] = http_resp

# ----------------------------
# Enhanced Analysis Functions (same as original but optimized)
# ----------------------------
def get_geolocation(ip):
    """Get comprehensive geolocation data"""
    if ip == "127.0.0.1" or ip.startswith(("192.168.", "10.", "172.")):
        return {
            "country": "Local Network", "city": "Local", "region": "Local",
            "isp": "Local Network", "asn": "Local", "timezone": "Local",
            "lat": 0, "lon": 0, "threat_level": "LOW"
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
    except:
        pass
    return {"country": "Unknown", "city": "Unknown", "region": "Unknown", "isp": "Unknown", "threat_level": "UNKNOWN"}

def detect_attack_tools(request_data):
    """Detect specific attack tools"""
    request_str = request_data.decode(errors="ignore")
    tools_detected = []
    
    tool_signatures = {
        'nmap': ['nmap', 'nmaplowercheck', 'nmapuppercheck'],
        'sqlmap': ['sqlmap', 'User-Agent: sqlmap'],
        'hydra': ['hydra', 'THC-Hydra'],
        'metasploit': ['metasploit', 'meterpreter', 'msf'],
        'nikto': ['nikto'],
        'gobuster': ['gobuster'],
        'burp': ['burp suite', 'burp'],
        'masscan': ['masscan'],
        'curl': ['curl/'],
        'wget': ['wget/'],
        'shodan': ['shodan'],
        'censys': ['censys']
    }
    
    for tool, signatures in tool_signatures.items():
        if any(sig in request_str.lower() for sig in signatures):
            tools_detected.append(tool.upper())
    
    return tools_detected

def log_event(ip, port, request_data, source_port=None):
    """Enhanced logging for cellular honeyport"""
    geo_info = get_geolocation(ip)
    tools_detected = detect_attack_tools(request_data)
    
    # Extract real attacker IP from ngrok headers
    real_ip = ip
    request_str = request_data.decode(errors="ignore")
    if "X-Forwarded-For:" in request_str:
        forwarded_match = re.search(r'X-Forwarded-For:\s*([^\r\n]+)', request_str)
        if forwarded_match:
            real_ip = forwarded_match.group(1).strip()
            geo_info = get_geolocation(real_ip)
    
    event = {
        "timestamp": datetime.now().isoformat(),
        "cellular_honeyport": True,
        "tunnel_connection": True,
        "attacker_identification": {
            "source_ip": real_ip,
            "tunnel_ip": ip,
            "source_port": source_port,
            "geolocation": geo_info
        },
        "connection_info": {
            "target_port": port,
            "protocol": get_protocol_name(port),
            "bytes_transferred": len(request_data)
        },
        "attack_analysis": {
            "detected_tools": tools_detected,
            "payload": request_data.decode(errors="ignore")[:500],
            "payload_size": len(request_data)
        },
        "threat_assessment": {
            "threat_level": calculate_threat_level(tools_detected, geo_info),
            "attack_vector": "Internet tunnel",
            "discovery_method": "ngrok tunnel scanning"
        }
    }
    
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event, indent=2) + "\n")
    
    # Console output
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🚨 CELLULAR ATTACK DETECTED")
    print(f"    📍 REAL IP: {real_ip} -> Port {port}")
    print(f"    🌍 LOCATION: {geo_info.get('city', 'Unknown')}, {geo_info.get('country', 'Unknown')}")
    if tools_detected:
        print(f"    🔧 TOOLS: {', '.join(tools_detected)}")

def get_protocol_name(port):
    """Get protocol name for port"""
    protocol_map = {
        2222: "SSH", 2323: "Telnet", 8080: "HTTP", 8443: "HTTPS",
        2121: "FTP", 2525: "SMTP", 3306: "MySQL", 5432: "PostgreSQL",
        1433: "MSSQL", 3389: "RDP", 4445: "SMB", 1135: "RPC", 1139: "NetBIOS"
    }
    return protocol_map.get(port, "Unknown")

def calculate_threat_level(tools, geo_info):
    """Calculate threat level"""
    if tools and any(tool in ['METASPLOIT', 'SQLMAP', 'HYDRA'] for tool in tools):
        return "CRITICAL"
    elif tools:
        return "HIGH"
    elif geo_info.get('threat_level') == 'HIGH':
        return "HIGH"
    else:
        return "MEDIUM"

# ----------------------------
# Connection Handler
# ----------------------------
def handle_client(conn, addr, port):
    ip, prt = addr
    conn.settimeout(5)
    req_data = b""
    try:
        req_data = conn.recv(4096)
        if port in RESPONSES:
            conn.sendall(RESPONSES[port])
    except:
        pass
    finally:
        conn.close()
    
    log_event(ip, port, req_data, prt)

# ----------------------------
# Port Listener
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
# Signal handlers
# ----------------------------
def signal_handler(sig, frame):
    print(f"\n[!] Shutting down cellular honeyport...")
    subprocess.run(["pkill", "-f", "ngrok"], capture_output=True)
    print("[*] Cellular honeyport stopped")
    sys.exit(0)

# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("=" * 60)
    print("📱 CELLULAR NETWORK HONEYPORT SYSTEM")
    print("=" * 60)
    print(f"📡 Host: {HOST} (Cellular Network)")
    print(f"📝 Log File: {LOG_FILE}")
    
    # Start tunnel manager
    tunnel_manager = TunnelManager()
    tunnel_manager.start_all_tunnels()
    tunnel_manager.save_tunnel_info()
    
    print("\n🔍 Services:")
    for port, banner_file in PORTS.items():
        protocol = get_protocol_name(port)
        print(f"   • {protocol} on port {port}")
    print("=" * 60)
    
    # Start listeners
    for port in PORTS:
        try:
            threading.Thread(target=start_listener, args=(port,), daemon=True).start()
        except Exception as e:
            print(f"[-] Failed to start listener on port {port}: {e}")
    
    print("[*] All listeners started. Tunnels active.")
    print("[*] Attackers can now reach your honeyport via ngrok tunnels!")
    print("[*] Press Ctrl+C to stop")
    
    # Keep running
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
