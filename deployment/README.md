# Perseus Deployment Guide

## 🚀 Quick Deployment

```bash
# Standard deployment (code updates only)
./deployment/deploy.sh

# Full deployment (first time or after major changes)
./deployment/deploy.sh --full
```

## 📋 Prerequisites

1. **SSH Access**: Ensure you have the SSH private key
   - Key location: `~/.ssh/extractreq_terraform`
   - Or set custom key: `export SSH_KEY=/path/to/key`

2. **Droplet IP**: Default is `157.245.84.180`
   - Or set custom IP: `export DROPLET_IP=your.ip.here`

3. **Git Access**: Ensure you have committed and pushed your changes
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```

## 🛠️ Architecture

### Server Configuration
- **OS**: Ubuntu 22.04 LTS
- **Resources**: 2 vCPUs, 4GB RAM (s-2vcpu-4gb)
- **Location**: `/opt/perseus/`
- **User**: `perseus` (service runs under this user)
- **Root User**: `root` (for deployments)

### Services
- **Backend**: Uvicorn with 4 workers
- **Redis**: Cache server on localhost:6379
- **Nginx**: Reverse proxy
- **Systemd**: Service management

### Key Files
- Service: `/etc/systemd/system/perseus-backend.service`
- Environment: `/opt/perseus/Backend/.env`
- Code: `/opt/perseus/Backend/app/`
- Logs: `journalctl -u perseus-backend`

## 📊 Performance Configuration

### Workers
The backend runs with **4 Uvicorn workers** for concurrent request handling.

### Redis Cache
- **LLM Descriptions**: 7 days TTL
- **Play Store Scraping**: 12 hours TTL
- **ML Predictions**: 24 hours TTL

### Environment Variables
```bash
# API Configuration
WORKERS=4
HOST=0.0.0.0
PORT=8000

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Cache TTL Configuration (seconds)
CACHE_TTL_LLM=604800       # 7 days
CACHE_TTL_SCRAPING=43200   # 12 hours
CACHE_TTL_ML=86400          # 24 hours

# API Keys (configure these)
HUGGINGFACE_TOKEN=your_token_here
GROQ_API_KEY=your_key_here
```

## 🔧 Manual Deployment Steps

If you prefer manual deployment:

### 1. Connect to Droplet
```bash
ssh -i ~/.ssh/extractreq_terraform root@157.245.84.180
```

### 2. Update Code
```bash
cd /tmp
git clone https://github.com/SAMUEL-ST-16/Perseus_Usabilidad.git perseus-update
cp -r perseus-update/Backend/app/* /opt/perseus/Backend/app/
cp perseus-update/Backend/requirements.txt /opt/perseus/Backend/
```

### 3. Update Dependencies
```bash
cd /opt/perseus/Backend
su - perseus -c 'cd /opt/perseus/Backend && source venv/bin/activate && pip install -r requirements.txt'
```

### 4. Update Configuration
```bash
# Edit .env if needed
nano /opt/perseus/Backend/.env

# Update systemd service if needed
nano /etc/systemd/system/perseus-backend.service
```

### 5. Restart Service
```bash
systemctl daemon-reload
systemctl restart perseus-backend
systemctl status perseus-backend
```

### 6. Verify
```bash
curl http://localhost:8000/health
curl http://157.245.84.180/health
```

## 🩺 Health Checks & Monitoring

### Check Service Status
```bash
ssh -i ~/.ssh/extractreq_terraform root@157.245.84.180 "systemctl status perseus-backend"
```

### View Logs
```bash
ssh -i ~/.ssh/extractreq_terraform root@157.245.84.180 "journalctl -u perseus-backend -f"
```

### Check Redis
```bash
ssh -i ~/.ssh/extractreq_terraform root@157.245.84.180 "redis-cli info | grep -E '(redis_version|connected_clients|used_memory_human)'"
```

### View Cache Keys
```bash
ssh -i ~/.ssh/extractreq_terraform root@157.245.84.180 "redis-cli KEYS 'perseus:*'"
```

### Check Workers
```bash
ssh -i ~/.ssh/extractreq_terraform root@157.245.84.180 "ps aux | grep uvicorn"
```

### Test API
```bash
# Health check
curl http://157.245.84.180/health

# Test analysis endpoint
curl -X POST http://157.245.84.180/api/requirements/analyze/single \
  -H "Content-Type: application/json" \
  -d '{"text":"La app debe cifrar las contraseñas"}'
```

## 🐛 Troubleshooting

### Service Won't Start
```bash
# Check logs
journalctl -u perseus-backend -n 100 --no-pager

# Check if port is in use
ss -tlnp | grep 8000

# Verify Python environment
su - perseus -c 'cd /opt/perseus/Backend && source venv/bin/activate && python --version'
```

### Redis Issues
```bash
# Check Redis status
systemctl status redis-server

# Test Redis connection
redis-cli ping

# View Redis logs
journalctl -u redis-server -n 50
```

### High Memory Usage
```bash
# Check memory
free -h

# Check process memory
ps aux --sort=-%mem | head -10

# Clear Redis cache if needed
redis-cli FLUSHDB
```

### Workers Not Starting
```bash
# Check systemd service configuration
systemctl cat perseus-backend

# Verify environment file
cat /opt/perseus/Backend/.env | grep WORKERS

# Check user permissions
ls -la /opt/perseus/Backend/
```

## 🔄 Rollback

If deployment fails, rollback to previous version:

```bash
# List backups
ssh -i ~/.ssh/extractreq_terraform root@157.245.84.180 "ls -lt /opt/perseus/Backend/app.backup.*"

# Restore backup
ssh -i ~/.ssh/extractreq_terraform root@157.245.84.180 "
  cd /opt/perseus/Backend &&
  rm -rf app &&
  cp -r app.backup.YYYYMMDD_HHMMSS app &&
  systemctl restart perseus-backend
"
```

## 📈 Performance Metrics

### Expected Response Times (with cache)
- **Single comment analysis**: 2-5s (first time), <1s (cached)
- **CSV 30 comments**: 11-33s (first time), 2-5s (cached)
- **Play Store scraping**: 42-124s (first time), <2s (cached)

### Concurrent Request Capacity
- **Without cache**: 4-8 requests/minute
- **With cache (70% hit rate)**: 20+ requests/minute

### Resource Usage
- **CPU**: ~30-50% with 4 workers under load
- **Memory**: ~1.5-2.5GB (includes ML models)
- **Redis Memory**: <100MB typically

## 🔐 Security Notes

1. **SSH Keys**: Never commit SSH keys to repository
2. **Environment Variables**: Keep `.env` with secrets out of git
3. **API Keys**: Rotate API keys regularly
4. **Firewall**: Only ports 22, 80, 443 exposed
5. **Updates**: Keep system packages updated

## 📞 Support

For issues or questions:
1. Check logs: `journalctl -u perseus-backend`
2. Verify health endpoint: `curl http://157.245.84.180/health`
3. Check Redis: `redis-cli ping`
4. Review this guide's troubleshooting section

---

**Last Updated**: December 2025
**Droplet**: perseus-server (157.245.84.180)
**Infrastructure**: DigitalOcean (nyc1)
