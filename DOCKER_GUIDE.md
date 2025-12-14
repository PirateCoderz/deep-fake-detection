# Docker Deployment Guide

This guide explains how to deploy the Fake Product Detection system using Docker.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 4GB RAM available
- Trained model file at `models/product_classifier.keras`

## Quick Start

### Development Mode (with hot-reload)

```bash
# Start all services in development mode
docker-compose -f docker-compose.dev.yml up

# Or run in background
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop services
docker-compose -f docker-compose.dev.yml down
```

### Production Mode

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

## Configuration

### Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Key variables:
- `POSTGRES_PASSWORD`: Database password (change for production!)
- `CORS_ORIGINS`: Allowed frontend origins
- `RATE_LIMIT_PER_HOUR`: API rate limit per IP
- `CONFIDENCE_THRESHOLD`: Minimum confidence for classification

### Production Configuration

For production deployment:

1. **Update CORS origins**:
   ```
   CORS_ORIGINS=https://yourdomain.com
   ```

2. **Change database password**:
   ```
   POSTGRES_PASSWORD=your_secure_password_here
   ```

3. **Set API URL**:
   ```
   NEXT_PUBLIC_API_URL=https://api.yourdomain.com
   ```

4. **Enable HTTPS** (recommended):
   - Use a reverse proxy (Nginx, Traefik, Caddy)
   - Configure SSL certificates
   - Update CORS_ORIGINS to use https://

## Services

The Docker Compose setup includes:

### Database (PostgreSQL)
- Port: 5432
- Persistent volume: `postgres_data`
- Health check enabled

### Cache (Redis)
- Port: 6379
- Persistent volume: `redis_data`
- AOF persistence enabled

### Backend API (FastAPI)
- Port: 8000
- 4 Gunicorn workers with Uvicorn
- Health check: `/api/v1/health`
- Automatic startup cleanup

### Frontend (Next.js + Nginx)
- Port: 3000
- Nginx reverse proxy
- Static file caching
- Security headers enabled

## Networking

All services communicate through the `fakedetect-network` bridge network:
- Services can reference each other by name (e.g., `http://backend:8000`)
- External access only through exposed ports

## Volumes

### Persistent Volumes
- `postgres_data`: Database files
- `redis_data`: Redis persistence
- `temp_uploads`: Temporary image uploads (auto-cleanup)

### Bind Mounts (Production)
- `./models:/app/models:ro` - Model files (read-only)

### Bind Mounts (Development)
- `./backend/src:/app/src:ro` - Backend code (hot-reload)
- `./frontend/src:/app/src:ro` - Frontend code (hot-reload)

## Health Checks

All services include health checks:

```bash
# Check service health
docker-compose ps

# View specific service health
docker inspect fakedetect-backend | grep -A 10 Health
```

## Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose logs backend

# Common issues:
# - Model file missing: Ensure models/product_classifier.keras exists
# - Database not ready: Wait for db health check to pass
# - Port conflict: Change BACKEND_PORT in .env
```

### Frontend can't connect to backend
```bash
# Check CORS configuration
docker-compose logs backend | grep CORS

# Verify API URL
docker-compose exec frontend env | grep API_URL

# Test backend from frontend container
docker-compose exec frontend wget -O- http://backend:8000/api/v1/health
```

### Database connection errors
```bash
# Check database is running
docker-compose ps db

# Test connection
docker-compose exec backend python -c "from src.database import engine; engine.connect()"

# Reset database (WARNING: deletes data)
docker-compose down -v
docker-compose up -d db
```

### Out of memory
```bash
# Check resource usage
docker stats

# Reduce Gunicorn workers in backend/Dockerfile:
# Change: -w 4 to -w 2
```

## Scaling

### Scale backend workers
```bash
# Run multiple backend instances
docker-compose up -d --scale backend=3

# Note: Requires load balancer configuration
```

### Resource limits
Add to docker-compose.yml:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

## Maintenance

### Backup database
```bash
# Create backup
docker-compose exec db pg_dump -U postgres fakedetect > backup.sql

# Restore backup
docker-compose exec -T db psql -U postgres fakedetect < backup.sql
```

### Update application
```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build

# Or rebuild specific service
docker-compose up -d --build backend
```

### Clean up old images
```bash
# Remove unused images
docker image prune -a

# Remove all stopped containers
docker container prune

# Remove unused volumes
docker volume prune
```

### View resource usage
```bash
# Real-time stats
docker stats

# Disk usage
docker system df
```

## Security Best Practices

1. **Change default passwords** in production
2. **Use HTTPS** with valid SSL certificates
3. **Restrict CORS origins** to your domain only
4. **Keep images updated**: `docker-compose pull`
5. **Run as non-root user** (already configured)
6. **Limit resource usage** with deploy constraints
7. **Enable firewall** rules for exposed ports
8. **Regular backups** of database and models
9. **Monitor logs** for suspicious activity
10. **Use secrets management** for sensitive data

## Monitoring

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Access containers
```bash
# Backend shell
docker-compose exec backend bash

# Database shell
docker-compose exec db psql -U postgres fakedetect

# Redis CLI
docker-compose exec redis redis-cli
```

## Production Deployment Checklist

- [ ] Update `.env` with production values
- [ ] Change database password
- [ ] Configure CORS for production domain
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set up automated backups
- [ ] Configure monitoring/alerting
- [ ] Test health checks
- [ ] Load test the application
- [ ] Document recovery procedures
- [ ] Set up log aggregation
- [ ] Configure resource limits

## Support

For issues or questions:
1. Check logs: `docker-compose logs`
2. Verify health: `docker-compose ps`
3. Review this guide
4. Check project README.md
