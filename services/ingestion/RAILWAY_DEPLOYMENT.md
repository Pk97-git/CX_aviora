# Deploying Ingestion Service to Railway

## Prerequisites

1. Railway account (sign up at https://railway.app)
2. Railway CLI installed
3. GitHub repository with the code

## Step 1: Install Railway CLI

```powershell
npm install -g @railway/cli
```

## Step 2: Login to Railway

```powershell
railway login
```

This will open a browser window for authentication.

## Step 3: Initialize Railway Project

```powershell
cd c:\Users\PrashanthKumar\Desktop\CX\aivora\services\ingestion
railway init
```

Select:

- Create a new project
- Name: `aivora-ingestion-service`

## Step 4: Link to GitHub (Optional but Recommended)

```powershell
# Push code to GitHub first
git add .
git commit -m "Add Railway deployment config"
git push origin main

# Then link in Railway dashboard:
# 1. Go to https://railway.app/dashboard
# 2. Select your project
# 3. Settings → Connect to GitHub
# 4. Select repository: Pk97-git/CX_aviora
# 5. Root directory: services/ingestion
```

## Step 5: Set Environment Variables

```powershell
# Database
railway variables set DATABASE_URL="postgresql://neondb_owner:npg_PV8mUupGQMB1@ep-young-snow-a1h4us5d-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Redis
railway variables set REDIS_URL="rediss://default:AWe7AAIncDJjZDNhMDAxMmQzZjY0OTQzOTliYzMyYTViNGUxNWY5ZnAyMjY1NTU@sterling-ant-26555.upstash.io:6379"

# Port (Railway will set this automatically, but we can set default)
railway variables set PORT="8080"

# Webhook Secrets (optional for now, can add later)
railway variables set FRESHDESK_WEBHOOK_SECRET=""
railway variables set ZENDESK_WEBHOOK_SECRET=""

# Rate Limiting
railway variables set RATE_LIMIT_PER_MINUTE="100"

# Circuit Breaker
railway variables set CIRCUIT_BREAKER_THRESHOLD="5"
railway variables set CIRCUIT_BREAKER_TIMEOUT="30"
```

## Step 6: Deploy

### Option A: Deploy from CLI

```powershell
railway up
```

### Option B: Deploy from GitHub (Recommended)

1. Push code to GitHub
2. Railway will automatically detect changes and deploy
3. Every push to `main` branch will trigger a new deployment

## Step 7: Monitor Deployment

```powershell
# View logs
railway logs

# Check status
railway status

# Open in browser
railway open
```

## Step 8: Get Your Service URL

```powershell
railway domain
```

Or check in Railway dashboard → Settings → Domains

Your service will be available at: `https://aivora-ingestion-service.up.railway.app`

## Step 9: Test Deployed Service

```powershell
# Health check
curl https://your-service.up.railway.app/health

# Metrics
curl https://your-service.up.railway.app/metrics

# Test webhook
curl -X POST https://your-service.up.railway.app/api/v1/ingest/webhook/freshdesk \
  -H "Content-Type: application/json" \
  -d '{"subject": "Test from Railway", "id": 12345}'
```

## Step 10: Configure Webhooks in Freshdesk/Zendesk

### Freshdesk

1. Go to Admin → Webhooks
2. Create new webhook
3. URL: `https://your-service.up.railway.app/api/v1/ingest/webhook/freshdesk`
4. Events: Ticket Created, Ticket Updated

### Zendesk

1. Go to Admin → Extensions → Targets
2. Create HTTP Target
3. URL: `https://your-service.up.railway.app/api/v1/ingest/webhook/zendesk`
4. Method: POST

## Monitoring

### View Logs

```powershell
railway logs --follow
```

### View Metrics

Access Prometheus metrics at:

```
https://your-service.up.railway.app/metrics
```

### Set Up Alerts (Optional)

Configure Railway to send alerts on:

- Deployment failures
- High memory usage
- Crash loops

## Troubleshooting

### Build Fails

```powershell
# Check logs
railway logs

# Common issues:
# 1. Go version mismatch - Check nixpacks.toml
# 2. Missing dependencies - Run go mod tidy locally first
# 3. Environment variables - Verify all required vars are set
```

### Service Crashes

```powershell
# Check logs for errors
railway logs --tail 100

# Common issues:
# 1. Database connection - Verify DATABASE_URL
# 2. Redis connection - Verify REDIS_URL
# 3. Port binding - Railway sets PORT automatically
```

### Health Check Fails

```powershell
# Verify health endpoint
curl https://your-service.up.railway.app/health

# Check Railway dashboard for health check status
```

## Cost Management

Railway free tier includes:

- $5 credit per month
- 500 hours of execution time
- 100 GB bandwidth

Monitor usage in Railway dashboard → Usage

## Scaling

To scale horizontally:

1. Railway dashboard → Settings
2. Increase replicas (paid feature)
3. Configure load balancing

## CI/CD

Railway automatically deploys on:

- Push to main branch
- Pull request merges
- Manual trigger from dashboard

## Rollback

```powershell
# View deployments
railway deployments

# Rollback to previous deployment
railway rollback <deployment-id>
```

## Environment-Specific Deployments

### Staging

```powershell
railway environment create staging
railway environment use staging
railway up
```

### Production

```powershell
railway environment create production
railway environment use production
railway up
```

## Next Steps

1. ✅ Deploy service to Railway
2. ✅ Configure environment variables
3. ✅ Test all endpoints
4. ✅ Configure webhooks in Freshdesk/Zendesk
5. ⏳ Set up monitoring/alerting
6. ⏳ Configure custom domain (optional)
7. ⏳ Set up staging environment
