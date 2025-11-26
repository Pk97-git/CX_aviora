# Deploy to Render.com (Free Alternative to Railway)

## ✅ Why Render?

- **Free Tier**: 750 hours/month (enough for 1 service 24/7)
- **Auto-deploy from GitHub**: Just like Railway
- **No credit card required** for free tier
- **Built-in SSL certificates**
- **Easy environment variable management**

---

## 🚀 Deploy in 5 Minutes

### Step 1: Sign Up for Render

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended)

### Step 2: Create New Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub account if not already connected
3. Select repository: **Pk97-git/CX_aviora**
4. Click "Connect"

### Step 3: Configure Service

Fill in these details:

**Name**: `aivora-ingestion-service`

**Region**: Singapore (closest to your Neon database)

**Branch**: `main`

**Root Directory**: `services/ingestion`

**Runtime**: `Go`

**Build Command**:

```
go build -o ingestion-service ./cmd/server
```

**Start Command**:

```
./ingestion-service
```

**Instance Type**: `Free`

### Step 4: Add Environment Variables

Click "Advanced" → "Add Environment Variable"

Add these variables:

```
DATABASE_URL=postgresql://neondb_owner:npg_PV8mUupGQMB1@ep-young-snow-a1h4us5d-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

REDIS_URL=rediss://default:AWe7AAIncDJjZDNhMDAxMmQzZjY0OTQzOTliYzMyYTViNGUxNWY5ZnAyMjY1NTU@sterling-ant-26555.upstash.io:6379

PORT=10000

RATE_LIMIT_PER_MINUTE=100

CIRCUIT_BREAKER_THRESHOLD=5

CIRCUIT_BREAKER_TIMEOUT=30

FRESHDESK_WEBHOOK_SECRET=

ZENDESK_WEBHOOK_SECRET=
```

**Important**: Render uses port 10000 by default, not 8080!

### Step 5: Configure Health Check

**Health Check Path**: `/health`

### Step 6: Deploy

Click "Create Web Service"

Render will:

1. Clone your repository
2. Build the Go application
3. Deploy to their infrastructure
4. Assign a public URL

**Build time**: ~3-5 minutes

---

## 🧪 Test Your Deployment

Your service will be available at:

```
https://aivora-ingestion-service.onrender.com
```

### Health Check

```
https://aivora-ingestion-service.onrender.com/health
```

### Metrics

```
https://aivora-ingestion-service.onrender.com/metrics
```

### Test Webhook

```powershell
$url = "https://aivora-ingestion-service.onrender.com"
Invoke-RestMethod -Uri "$url/api/v1/ingest/webhook/freshdesk" -Method Post -Body '{"subject": "Render Test", "id": 99999}' -ContentType "application/json"
```

---

## 📊 Free Tier Limits

- **Hours**: 750 hours/month (31 days × 24 hours = 744 hours)
- **Memory**: 512 MB
- **CPU**: Shared
- **Bandwidth**: 100 GB/month
- **Build minutes**: 500 minutes/month

**Perfect for this service!** ✅

---

## ⚠️ Important Notes

### 1. Sleep on Inactivity

Free tier services sleep after 15 minutes of inactivity.

- **First request after sleep**: ~30 seconds to wake up
- **Solution**: Use a cron job to ping `/health` every 10 minutes

### 2. Port Configuration

Render uses port 10000, not 8080. Our service reads from `PORT` env var, so it will work automatically.

### 3. Auto-Deploy

Every push to `main` branch automatically deploys to Render.

---

## 🔄 Keep Service Awake (Optional)

Create a cron job to ping your service every 10 minutes:

### Using cron-job.org (Free)

1. Go to https://cron-job.org
2. Create account
3. Add new cron job:
   - **URL**: `https://aivora-ingestion-service.onrender.com/health`
   - **Schedule**: Every 10 minutes
   - **Method**: GET

This prevents the service from sleeping!

---

## 📈 Monitoring

### Render Dashboard

- **Logs**: Real-time streaming
- **Metrics**: CPU, Memory, Network
- **Deployments**: History and manual redeploy
- **Events**: Build and deploy events

### Access Logs

```
# In Render dashboard
Services → aivora-ingestion-service → Logs
```

---

## 🆙 Upgrade Options

If you need more:

- **Starter**: $7/month (no sleep, 1 GB RAM)
- **Standard**: $25/month (2 GB RAM, priority support)

---

## ✅ Deployment Checklist

- [ ] Signed up for Render
- [ ] Connected GitHub repository
- [ ] Configured build and start commands
- [ ] Added all environment variables
- [ ] Set health check path
- [ ] Deployed service
- [ ] Tested health endpoint
- [ ] Tested webhook endpoint
- [ ] Configured cron job (optional)
- [ ] Updated Freshdesk/Zendesk webhooks

---

## 🔗 Useful Links

- **Render Dashboard**: https://dashboard.render.com
- **Render Docs**: https://render.com/docs
- **Your Service**: https://aivora-ingestion-service.onrender.com

---

**Deployment Method**: GitHub Integration
**Cost**: $0/month (Free tier)
**Build Time**: 3-5 minutes
**Auto-Deploy**: ✅ Enabled
**Status**: Ready to deploy!
