# BlockLure-AI - Advanced Honeypot System

An intelligent honeypot system designed to detect, analyze, and respond to cyber attacks in real-time.

## Features

- **Multi-Protocol Support**: SSH, HTTP, RDP, MySQL honeypots
- **Real-time Dashboard**: Web-based monitoring and analytics
- **Geolocation Tracking**: Track attacker locations
- **Automated Blocking**: Firewall integration for threat response
- **Attack Analytics**: Detailed logging and visualization
- **Attacker Engagement**: Fake services to gather intelligence

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   cd dashboard/frontend && npm install
   ```

2. **Configure**:
   Edit `honeyport-core/config.yaml` for your environment

3. **Run**:
   ```bash
   python honeyport-core/honeyport.py
   ```

4. **Access Dashboard**:
   Open http://localhost:8080

## Architecture

- `honeyport-core/`: Main honeypot engine
- `dashboard/`: Web interface for monitoring
- `infra/`: Docker and Kubernetes deployment
- `attacker-site/`: Fake website for engagement
- `data/`: Logs and database storage

## Security Notice

This system is designed for security research and network defense. Use responsibly and in compliance with local laws.
