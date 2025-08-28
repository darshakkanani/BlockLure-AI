# 🍯 BlockLure-AI Advanced Honeyport System

A sophisticated multi-protocol honeyport system designed to detect, log, and analyze cyber attacks across multiple network protocols.

## 🚀 Features

### Multi-Protocol Support
- **SSH** (Port 2222) - Fake SSH server with realistic banners
- **Telnet** (Port 2323) - Interactive telnet login simulation  
- **SMB** (Port 4445) - Windows file sharing honeypot
- **MySQL** (Port 3306) - Database server simulation
- **HTTP** (Port 8080) - Fake corporate login portal

### Advanced Threat Detection
- **Nmap Scanning Detection** - Identifies network reconnaissance
- **SQL Injection Analysis** - Detects database attack attempts
- **Directory Traversal** - Path manipulation attack detection
- **Brute Force Detection** - Credential stuffing identification
- **Web Vulnerability Scanning** - Common exploit path detection

### Comprehensive Intelligence Gathering
- **Geolocation Tracking** - Country, city, ISP identification
- **Credential Harvesting** - Captures login attempts
- **Attack Pattern Analysis** - Methodology classification
- **Threat Level Assessment** - Automated risk scoring
- **Real-time Alerting** - Console notifications for threats

## 📁 Project Structure

```
Honeyport/
├── honeyport.py          # Main honeyport engine
├── banners/
│   ├── ssh.txt          # SSH banner response
│   ├── telnet.txt       # Telnet login prompt
│   ├── smb.txt          # SMB protocol response
│   └── mysql.txt        # MySQL handshake
├── fake_http.html       # Corporate login page
├── honeyport.log        # Attack intelligence logs
└── README.md           # This file
```

## 🔧 Installation & Usage

### Prerequisites
```bash
pip install requests
```

### Running the Honeyport
```bash
python3 honeyport.py
```

### Testing Connections
```bash
# Test SSH
ssh -p 2222 admin@localhost

# Test Telnet  
telnet localhost 2323

# Test HTTP
curl http://localhost:8080

# Test with Nmap
nmap -p 2222,2323,3306,4445,8080 localhost
```

## 📊 Log Analysis

The system generates comprehensive JSON logs in `honeyport.log`:

```json
{
  "timestamp": "2024-01-01T12:00:00",
  "connection_info": {
    "source_ip": "192.168.1.100",
    "target_port": 2222,
    "protocol": "SSH"
  },
  "geolocation": {
    "country": "Russia",
    "city": "Moscow",
    "isp": "Evil Corp"
  },
  "attack_analysis": {
    "attack_patterns": ["NMAP_SCAN", "BRUTE_FORCE"],
    "methodology": ["Network reconnaissance", "Credential attack"],
    "threat_level": "HIGH",
    "is_automated": true
  },
  "request_data": {
    "extracted_credentials": {
      "username": "admin",
      "password": "password123"
    }
  }
}
```

## 🛡️ Security Features

- **Non-privileged Ports** - Runs without root access
- **Geolocation Blocking** - Identify attack origins
- **Pattern Recognition** - Automated threat classification
- **Credential Monitoring** - Track stolen credentials
- **Real-time Alerts** - Immediate threat notifications

## 🎯 Attack Detection Capabilities

| Attack Type | Detection Method | Response |
|-------------|------------------|----------|
| Nmap Scans | Signature detection | Log + Alert |
| SQL Injection | Pattern matching | Log + Block |
| Brute Force | Connection analysis | Log + Monitor |
| Web Scanning | Path enumeration | Log + Trace |
| Directory Traversal | Path validation | Log + Alert |

## 📈 Monitoring Dashboard

Real-time console output provides immediate visibility:

```
[12:34:56] 192.168.1.100:2222 (SSH)
    🚨 THREATS: NMAP_SCAN, BRUTE_FORCE
    🔑 CREDS: {'username': 'admin', 'password': '123456'}
    🌍 LOCATION: Moscow, Russia
```

## 🔒 Best Practices

1. **Deploy in DMZ** - Isolate from production systems
2. **Monitor Logs** - Regular analysis of attack patterns
3. **Update Banners** - Keep responses realistic
4. **Backup Logs** - Preserve attack intelligence
5. **Network Segmentation** - Prevent lateral movement

## ⚠️ Legal Notice

This tool is for educational and authorized security testing only. Ensure compliance with local laws and obtain proper authorization before deployment.

## 🤝 Contributing

Contributions welcome! Please submit pull requests with:
- New protocol support
- Enhanced detection algorithms
- Improved logging formats
- Performance optimizations

---

**BlockLure-AI** - Advanced Cyber Deception Technology
