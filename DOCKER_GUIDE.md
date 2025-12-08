# Aivora Docker Deployment Guide

## Prerequisites

- Docker Desktop installed and running
- `.env` file in `services/intelligence/` with:
  - `DATABASE_URL`
  - `REDIS_URL`
  - `GROQ_API_KEY`

## Quick Start

### 1. Build and Start All Services

```bash
docker-compose up -d --build
```

### 2. Check Status

```bash
docker-compose ps
```

### 3. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f intelligence
docker-compose logs -f frontend
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Management Commands

### Stop Services

```bash
docker-compose down
```

### Restart Services

```bash
docker-compose restart
```

### Rebuild After Code Changes

```bash
docker-compose up -d --build
```

### Remove Everything (including volumes)

```bash
docker-compose down -v
```

## Troubleshooting

### Check Container Logs

```bash
docker-compose logs intelligence
```

### Enter Container Shell

```bash
docker-compose exec intelligence /bin/bash
docker-compose exec frontend /bin/sh
```

### Rebuild Single Service

```bash
docker-compose up -d --build intelligence
```

### Check Network Connectivity

```bash
docker-compose exec frontend ping intelligence
```

## Architecture

```
┌─────────────────┐
│   Frontend      │
│   (Port 3000)   │
│   Nginx + React │
└────────┬────────┘
         │
         │ HTTP Proxy
         │
┌────────▼────────┐
│  Intelligence   │
│   (Port 8000)   │
│   FastAPI       │
└────────┬────────┘
         │
         ├─────► Neon PostgreSQL (External)
         └─────► Upstash Redis (External)
```

## Environment Variables

The `docker-compose.yml` uses environment variables from:

1. `services/intelligence/.env` (mounted as env_file)
2. System environment variables (if set)

Required variables:

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `GROQ_API_KEY`: Groq API key for AI features

## Production Deployment

For production, consider:

1. Using Docker Swarm or Kubernetes
2. Setting up proper secrets management
3. Configuring SSL/TLS certificates
4. Setting up monitoring and logging
5. Implementing auto-scaling

## Notes

- Frontend uses nginx in production mode
- Backend runs with uvicorn
- Health checks ensure services start in correct order
- All services share a custom bridge network
- Containers restart automatically unless stopped
