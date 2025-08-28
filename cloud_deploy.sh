#!/bin/bash

# Cloud deployment script for honeyport
# This script helps deploy the honeyport to a VPS for internet exposure

echo "=== HONEYPORT CLOUD DEPLOYMENT HELPER ==="
echo ""
echo "This script will help you deploy your honeyport to a cloud VPS"
echo "for maximum internet exposure to attract attackers."
echo ""

# VPS providers and typical costs
echo "RECOMMENDED VPS PROVIDERS:"
echo "1. DigitalOcean - $5/month droplet"
echo "2. Linode - $5/month nanode"
echo "3. Vultr - $2.50/month instance"
echo "4. AWS EC2 - t2.micro (free tier)"
echo "5. Google Cloud - e2-micro (free tier)"
echo ""

echo "DEPLOYMENT STEPS:"
echo "1. Create a VPS instance with Ubuntu 20.04+"
echo "2. Copy honeyport files to VPS"
echo "3. Install Python dependencies"
echo "4. Configure firewall rules"
echo "5. Run honeyport as systemd service"
echo ""

echo "SECURITY CONSIDERATIONS:"
echo "- Use a dedicated VPS only for honeyport"
echo "- Enable SSH key authentication"
echo "- Change default SSH port"
echo "- Monitor system resources"
echo "- Set up log rotation"
echo ""

echo "To deploy manually:"
echo "scp -r Honeyport/ user@your-vps-ip:~/"
echo "ssh user@your-vps-ip"
echo "cd Honeyport && python3 honeyport.py"
