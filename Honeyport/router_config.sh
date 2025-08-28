#!/bin/bash

# Router configuration script for direct IP access
# This will help configure your router for port forwarding

echo "🔧 ROUTER CONFIGURATION FOR DIRECT IP ACCESS"
echo "=============================================="
echo ""
echo "Your Network Configuration:"
echo "• Local IP: 172.20.10.2"
echo "• Public IP: 42.111.213.10"
echo "• Router Gateway: 172.20.10.1"
echo ""

echo "📋 REQUIRED PORT FORWARDING RULES:"
echo "=================================="
echo "Configure these rules in your router at http://172.20.10.1"
echo ""
echo "External Port → Internal IP    → Internal Port → Protocol"
echo "2222         → 172.20.10.2    → 2222          → TCP"
echo "2323         → 172.20.10.2    → 2323          → TCP"
echo "3306         → 172.20.10.2    → 3306          → TCP"
echo "4445         → 172.20.10.2    → 4445          → TCP"
echo "8081         → 172.20.10.2    → 8081          → TCP"
echo ""

echo "🌐 AFTER CONFIGURATION, ATTACKERS CAN REACH:"
echo "============================================="
echo "SSH:    42.111.213.10:2222"
echo "Telnet: 42.111.213.10:2323"
echo "MySQL:  42.111.213.10:3306"
echo "SMB:    42.111.213.10:4445"
echo "HTTP:   http://42.111.213.10:8081"
echo ""

echo "🔧 ROUTER CONFIGURATION STEPS:"
echo "=============================="
echo "1. Open browser: http://172.20.10.1"
echo "2. Login with admin credentials"
echo "3. Find 'Port Forwarding' or 'Virtual Server' section"
echo "4. Add the port forwarding rules above"
echo "5. Save and restart router"
echo ""

echo "🧪 TEST COMMANDS (run after router config):"
echo "==========================================="
echo "nmap -p 2222,2323,3306,4445,8081 42.111.213.10"
echo "telnet 42.111.213.10 2222"
echo "curl http://42.111.213.10:8081"
echo ""

# Try to open router admin page
echo "🚀 Opening router configuration page..."
open http://172.20.10.1 2>/dev/null || echo "Please manually open: http://172.20.10.1"
