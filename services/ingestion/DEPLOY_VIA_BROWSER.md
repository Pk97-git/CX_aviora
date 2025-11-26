# Railway Deployment via GitHub - Visual Guide

## ✅ Code is Ready on GitHub!

**Repository**: https://github.com/Pk97-git/CX_aviora
**Commit**: 13848c3
**Path**: `services/ingestion/`

---

## 🚀 Deploy in 3 Minutes (Browser-Based)

### Step 1: Open Railway Dashboard

**URL**: https://railway.app/new

Click "Deploy from GitHub repo"

### Step 2: Connect GitHub

1. Click "Configure GitHub App"
2. Select "Pk97-git" account
3. Choose "CX_aviora" repository
4. Click "Install & Authorize"

### Step 3: Select Repository

1. Search for "CX_aviora"
2. Click on the repository
3. Railway will detect the `railway.json` file

### Step 4: Configure Deployment

1. **Root Directory**: `services/ingestion`
2. **Branch**: `main`
3. Click "Deploy Now"

### Step 5: Add Environment Variables

In Railway dashboard, go to Variables tab and add:

```
DATABASE_URL=postgresql://neondb_owner:***REMOVED***@ep-young-snow-a1h4us5d-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

REDIS_URL=rediss://default:AWe7AAIncDJjZDNhMDAxMmQzZjY0OTQzOTliYzMyYTViNGUxNWY5ZnAyMjY1NTU@sterling-ant-26555.upstash.io:6379

PORT=8080

RATE_LIMIT_PER_MINUTE=100

CIRCUIT_BREAKER_THRESHOLD=5

CIRCUIT_BREAKER_TIMEOUT=30

FRESHDESK_WEBHOOK_SECRET=

ZENDESK_WEBHOOK_SECRET=
```

### Step 6: Wait for Deployment

- Build time: ~2 minutes
- Watch logs in real-time
- Wait for "Deployment successful" message

### Step 7: Get Your URL

1. Go to "Settings" tab
2. Click "Generate Domain"
3. Copy the URL (e.g., `https://cx-aviora-production.up.railway.app`)

---

## 🧪 Test Your Deployment

### Health Check

```
https://your-url.up.railway.app/health
```

### Metrics

```
https://your-url.up.railway.app/metrics
```

### Test Webhook

```powershell
$url = "https://your-url.up.railway.app"
Invoke-RestMethod -Uri "$url/api/v1/ingest/webhook/freshdesk" -Method Post -Body '{"subject": "Railway Test", "id": 99999}' -ContentType "application/json"
```

---

## 📊 What's Deployed

✅ Production-ready Ingestion Service
✅ Webhook signature validation
✅ Idempotency
✅ Rate limiting (100 req/min)
✅ Prometheus metrics
✅ Redis circuit breaker
✅ Auto-scaling
✅ Health checks
✅ Connected to Neon PostgreSQL
✅ Connected to Upstash Redis

---

## 🔄 Auto-Deploy Enabled

Every push to `main` branch will automatically deploy to Railway!

```powershell
git add .
git commit -m "Update service"
git push origin main
# Railway automatically deploys
```

---

## 📱 Monitor Your Service

### Railway Dashboard

- **Metrics**: CPU, Memory, Network
- **Logs**: Real-time streaming
- **Deployments**: History and rollback
- **Usage**: Cost tracking

### Endpoints

- **Health**: `GET /health`
- **Metrics**: `GET /metrics`
- **Freshdesk**: `POST /api/v1/ingest/webhook/freshdesk`
- **Zendesk**: `POST /api/v1/ingest/webhook/zendesk`

---

## ✅ Success Checklist

After deployment, verify:

- [ ] Build completed successfully
- [ ] Deployment status: Running
- [ ] Health check returns 200 OK
- [ ] Metrics endpoint accessible
- [ ] Database connection working (check logs)
- [ ] Redis connection working (check logs)
- [ ] Test webhook creates ticket
- [ ] Domain generated and accessible

---

## 🎯 Next Steps

1. **Test all endpoints** using the URLs above
2. **Configure webhooks** in Freshdesk/Zendesk with your Railway URL
3. **Monitor logs** for any errors
4. **Set up alerts** in Railway dashboard
5. **Update documentation** with production URL

---

**Deployment Method**: GitHub Integration (Recommended)
**Auto-Deploy**: ✅ Enabled
**Estimated Cost**: $3-4/month
**Build Time**: ~2 minutes
**Status**: Ready to deploy!
