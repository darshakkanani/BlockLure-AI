#!/bin/bash

# ngrok setup script for honeyport internet exposure
# This creates tunnels for all honeyport services

echo "🚀 Setting up ngrok tunnels for honeyport..."
echo ""

# Kill any existing ngrok processes
pkill -f ngrok

# Wait a moment for cleanup
sleep 2

echo "Starting ngrok tunnels for all honeyport services:"
echo ""

# Start tunnels for each service (background processes)
echo "📡 Starting SSH tunnel (port 2222)..."
ngrok tcp 2222 --log=stdout > /tmp/ngrok_ssh.log 2>&1 &
SSH_PID=$!

echo "📡 Starting Telnet tunnel (port 2323)..."
ngrok tcp 2323 --log=stdout > /tmp/ngrok_telnet.log 2>&1 &
TELNET_PID=$!

echo "📡 Starting MySQL tunnel (port 3306)..."
ngrok tcp 3306 --log=stdout > /tmp/ngrok_mysql.log 2>&1 &
MYSQL_PID=$!

echo "📡 Starting SMB tunnel (port 4445)..."
ngrok tcp 4445 --log=stdout > /tmp/ngrok_smb.log 2>&1 &
SMB_PID=$!

echo "📡 Starting HTTP tunnel (port 8081)..."
ngrok http 8081 --log=stdout > /tmp/ngrok_http.log 2>&1 &
HTTP_PID=$!

echo ""
echo "⏳ Waiting for tunnels to initialize..."
sleep 5

echo ""
echo "🌐 NGROK TUNNEL URLS:"
echo "===================="

# Extract URLs from log files
if [ -f /tmp/ngrok_ssh.log ]; then
    SSH_URL=$(grep -o 'tcp://[^[:space:]]*' /tmp/ngrok_ssh.log | head -1)
    echo "🔐 SSH (port 2222):    $SSH_URL"
fi

if [ -f /tmp/ngrok_telnet.log ]; then
    TELNET_URL=$(grep -o 'tcp://[^[:space:]]*' /tmp/ngrok_telnet.log | head -1)
    echo "📟 Telnet (port 2323): $TELNET_URL"
fi

if [ -f /tmp/ngrok_mysql.log ]; then
    MYSQL_URL=$(grep -o 'tcp://[^[:space:]]*' /tmp/ngrok_mysql.log | head -1)
    echo "🗄️  MySQL (port 3306):  $MYSQL_URL"
fi

if [ -f /tmp/ngrok_smb.log ]; then
    SMB_URL=$(grep -o 'tcp://[^[:space:]]*' /tmp/ngrok_smb.log | head -1)
    echo "📁 SMB (port 4445):    $SMB_URL"
fi

if [ -f /tmp/ngrok_http.log ]; then
    HTTP_URL=$(grep -o 'https://[^[:space:]]*' /tmp/ngrok_http.log | head -1)
    echo "🌐 HTTP (port 8081):   $HTTP_URL"
fi

echo ""
echo "📊 Process IDs:"
echo "SSH: $SSH_PID | Telnet: $TELNET_PID | MySQL: $MYSQL_PID | SMB: $SMB_PID | HTTP: $HTTP_PID"
echo ""
echo "🎯 Your honeyport is now exposed to the internet!"
echo "🚨 Attackers can now reach your services via these URLs"
echo ""
echo "To stop all tunnels: pkill -f ngrok"
echo "To view tunnel status: curl http://localhost:4040/api/tunnels"
echo ""
echo "Monitor attacks in real-time:"
echo "tail -f /Users/hunter/Desktop/BlockLure-AI/Honeyport/honeyport.log"
