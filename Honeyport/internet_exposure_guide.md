# Internet Exposure Guide for Honeyport

## Current Status
- **Local IP**: 172.20.10.2
- **Public IP**: 42.111.213.10
- **Router Gateway**: 172.20.10.1
- **Honeyport Ports**: 2222, 2323, 3306, 4445, 8081

## Method 1: Router Port Forwarding (Recommended)

### Step 1: Access Router Configuration
1. Open browser and go to: `http://172.20.10.1`
2. Login with admin credentials
3. Navigate to "Port Forwarding" or "Virtual Server" or "NAT"

### Step 2: Add Port Forwarding Rules
Create these forwarding rules:

| Service | External Port | Internal IP  | Internal Port | Protocol |
|---------|---------------|--------------|---------------|----------|
| SSH     | 2222          | 172.20.10.2  | 2222          | TCP      |
| Telnet  | 2323          | 172.20.10.2  | 2323          | TCP      |
| MySQL   | 3306          | 172.20.10.2  | 3306          | TCP      |
| SMB     | 4445          | 172.20.10.2  | 4445          | TCP      |
| HTTP    | 8081          | 172.20.10.2  | 8081          | TCP      |

### Step 3: Test Connectivity
After configuring port forwarding, test from external network:
```bash
# Test SSH honeyport
nc -zv 42.111.213.10 2222

# Test HTTP honeyport
curl http://42.111.213.10:8081
```

## Method 2: Cloud VPS Deployment

### Recommended VPS Providers
- **DigitalOcean**: $5/month droplet
- **Linode**: $5/month nanode  
- **Vultr**: $2.50/month instance
- **AWS EC2**: t2.micro (free tier)

### VPS Setup Commands
```bash
# 1. Create Ubuntu 20.04+ VPS
# 2. Upload honeyport files
scp -r Honeyport/ user@vps-ip:~/

# 3. SSH to VPS and setup
ssh user@vps-ip
sudo apt update && sudo apt install python3 python3-pip
pip3 install requests

# 4. Move to system directory
sudo mkdir /opt/honeyport
sudo cp -r ~/Honeyport/* /opt/honeyport/
sudo cp /opt/honeyport/honeyport.service /etc/systemd/system/

# 5. Start as system service
sudo systemctl daemon-reload
sudo systemctl enable honeyport
sudo systemctl start honeyport

# 6. Configure firewall
sudo ufw allow 2222/tcp
sudo ufw allow 2323/tcp
sudo ufw allow 3306/tcp
sudo ufw allow 4445/tcp
sudo ufw allow 8081/tcp
sudo ufw --force enable
```

## Method 3: ngrok Tunnel (Quick Test)

For immediate testing, use ngrok:
```bash
# Install ngrok
brew install ngrok

# Expose multiple ports (requires paid plan for multiple tunnels)
ngrok tcp 2222 &
ngrok tcp 2323 &
ngrok tcp 3306 &
ngrok tcp 4445 &
ngrok http 8081 &
```

## Security Considerations

### ⚠️ WARNING: Internet Exposure Risks
- **Only use dedicated machine/VPS** for honeyport
- **Never run on production systems**
- **Monitor system resources** - attacks can be resource intensive
- **Set up log rotation** to prevent disk space issues
- **Regular backups** of attack logs

### Enhanced Monitoring
Your honeyport already includes:
- ✅ Geolocation tracking
- ✅ Attack pattern analysis
- ✅ Tool detection
- ✅ Exploit attempt logging
- ✅ Comprehensive threat assessment

## Testing External Access

Once configured, test from external network:
```bash
# Test each service
nmap -p 2222,2323,3306,4445,8081 42.111.213.10
telnet 42.111.213.10 2222
curl http://42.111.213.10:8081
```

## Attracting More Attackers

### Shodan Exposure
Your services will be discovered by Shodan within 24-48 hours of exposure.

### Additional Exposure Methods
1. **Submit to threat intel feeds**
2. **Post on security forums** (as research)
3. **Use common service banners** (already implemented)
4. **Run on standard ports** if possible (requires root)

## Monitoring Commands

```bash
# Monitor real-time attacks
tail -f /path/to/honeyport.log

# Count attacks by IP
grep -o '"source_ip": "[^"]*"' honeyport.log | sort | uniq -c | sort -nr

# Monitor system resources
htop
df -h
```

Your honeyport is ready for internet exposure! Choose the method that works best for your setup.
