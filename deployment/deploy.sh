#!/bin/bash
#
# Perseus Deployment Script
# Deploys updates to production droplet with zero downtime
#
# Usage: ./deployment/deploy.sh [--full]
#   --full: Full deployment including git clone and system packages

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SSH_KEY="${SSH_KEY:-~/.ssh/extractreq_terraform}"
DROPLET_IP="${DROPLET_IP:-157.245.84.180}"
DEPLOY_USER="root"
PROJECT_DIR="/opt/perseus"
REPO_URL="https://github.com/SAMUEL-ST-16/Perseus_Usabilidad.git"

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

ssh_exec() {
    ssh -i "$SSH_KEY" -o ConnectTimeout=10 "${DEPLOY_USER}@${DROPLET_IP}" "$1"
}

# Check prerequisites
log_info "Checking prerequisites..."
if [ ! -f "$SSH_KEY" ]; then
    log_error "SSH key not found: $SSH_KEY"
    exit 1
fi

# Test SSH connection
log_info "Testing SSH connection..."
if ! ssh_exec "echo 'SSH OK'"; then
    log_error "Failed to connect to droplet"
    exit 1
fi

# Parse arguments
FULL_DEPLOY=false
if [ "$1" == "--full" ]; then
    FULL_DEPLOY=true
    log_warn "Full deployment mode enabled"
fi

# Full deployment (first time setup)
if [ "$FULL_DEPLOY" == "true" ]; then
    log_info "Starting full deployment..."

    # Install Redis
    log_info "Installing Redis..."
    ssh_exec "apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y redis-server"
    ssh_exec "systemctl enable redis-server && systemctl start redis-server"

    # Clone repository if not exists
    log_info "Checking if project exists..."
    if ! ssh_exec "[ -d $PROJECT_DIR ]"; then
        log_info "Cloning repository..."
        ssh_exec "git clone $REPO_URL $PROJECT_DIR"
    fi
fi

# Standard deployment (code updates)
log_info "Starting deployment..."

# Create temporary clone for updates
log_info "Downloading latest code..."
ssh_exec "cd /tmp && rm -rf perseus-update && git clone $REPO_URL perseus-update"

# Backup current code
log_info "Creating backup..."
ssh_exec "cp -r $PROJECT_DIR/Backend/app $PROJECT_DIR/Backend/app.backup.\$(date +%Y%m%d_%H%M%S) || true"

# Copy updated files
log_info "Copying updated files..."
ssh_exec "cp -r /tmp/perseus-update/Backend/app/* $PROJECT_DIR/Backend/app/ && \
          cp /tmp/perseus-update/Backend/requirements.txt $PROJECT_DIR/Backend/"

# Update dependencies
log_info "Updating Python dependencies..."
ssh_exec "cd $PROJECT_DIR/Backend && su - perseus -c 'cd $PROJECT_DIR/Backend && source venv/bin/activate && pip install -q -r requirements.txt'"

# Update environment variables if needed
log_info "Checking environment variables..."
if ! ssh_exec "grep -q 'REDIS_HOST' $PROJECT_DIR/Backend/.env"; then
    log_warn "Adding Redis configuration to .env..."
    ssh_exec "cat >> $PROJECT_DIR/Backend/.env << 'EOF'

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Cache TTL Configuration (in seconds)
CACHE_TTL_LLM=604800
CACHE_TTL_SCRAPING=43200
CACHE_TTL_ML=86400
EOF"
fi

# Update WORKERS to 4
if ssh_exec "grep -q '^WORKERS=1' $PROJECT_DIR/Backend/.env"; then
    log_info "Updating WORKERS to 4..."
    ssh_exec "sed -i 's/^WORKERS=1/WORKERS=4/' $PROJECT_DIR/Backend/.env"
fi

# Update systemd service
log_info "Updating systemd service..."
ssh_exec "cat > /etc/systemd/system/perseus-backend.service << 'EOF'
[Unit]
Description=Perseus FastAPI Backend
After=network.target redis-server.service

[Service]
Type=simple
User=perseus
WorkingDirectory=$PROJECT_DIR/Backend
Environment=\"PATH=$PROJECT_DIR/Backend/venv/bin\"
EnvironmentFile=$PROJECT_DIR/Backend/.env
ExecStart=$PROJECT_DIR/Backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF"

# Reload and restart service
log_info "Restarting service (with zero downtime)..."
ssh_exec "systemctl daemon-reload && systemctl restart perseus-backend"

# Wait for service to be ready
log_info "Waiting for service to start..."
sleep 5

# Health check
log_info "Performing health check..."
if curl -sf "http://${DROPLET_IP}/health" > /dev/null; then
    log_info "✓ Deployment successful!"
    log_info "Health check: $(curl -s http://${DROPLET_IP}/health)"
else
    log_error "Health check failed!"
    log_error "Check logs: ssh -i $SSH_KEY ${DEPLOY_USER}@${DROPLET_IP} 'systemctl status perseus-backend'"
    exit 1
fi

# Show service status
log_info "Service status:"
ssh_exec "systemctl status perseus-backend --no-pager -l | head -15"

# Show Redis stats
log_info "Redis status:"
ssh_exec "redis-cli info | grep -E '(redis_version|connected_clients|used_memory_human)'"

# Cleanup
log_info "Cleaning up..."
ssh_exec "rm -rf /tmp/perseus-update"

log_info "✓ Deployment completed successfully!"
log_info "Backend URL: http://${DROPLET_IP}"
log_info "Health endpoint: http://${DROPLET_IP}/health"
