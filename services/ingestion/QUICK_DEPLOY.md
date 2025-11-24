# Quick Railway Deployment Guide

## ⚡ Quick Start (5 Minutes)

### Step 1: Open PowerShell and Navigate

```powershell
cd c:\Users\PrashanthKumar\Desktop\CX\aivora\services\ingestion
$env:Path += ";$env:APPDATA\npm"
```

### Step 2: Login to Railway

```powershell
railway login
```

**Action**: Browser will open → Sign in with GitHub/Email

### Step 3: Create New Project

```powershell
railway init
```

**Action**:

- Select: "Create a new project"
- Name: `aivora-ingestion-service`

### Step 4: Set Environment Variables (Copy-Paste All)

```powershell
railway variables set DATABASE_URL="postgresql://neondb_owner:npg_PV8mUupGQMB1@ep-young-snow-a1h4us5d-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

railway variables set REDIS_URL="rediss://default:AWe7AAIncDJjZDNhMDAxMmQzZjY0OTQzOTliYzMyYTViNGUxNWY5ZnAyMjY1NTU@sterling-ant-26555.upstash.io:6379"

railway variables set PORT="8080"

railway variables set RATE_LIMIT_PER_MINUTE="100"

railway variables set CIRCUIT_BREAKER_THRESHOLD="5"

railway variables set CIRCUIT_BREAKER_TIMEOUT="30"

railway variables set FRESHDESK_WEBHOOK_SECRET=""

railway variables set ZENDESK_WEBHOOK_SECRET=""
```

### Step 5: Deploy

```powershell
railway up
```

**Wait**: 2-3 minutes for build and deployment

### Step 6: Get Your Service URL

```powershell
railway domain
```

### Step 7: Test Deployment

```powershell
# Replace YOUR-URL with the URL from step 6
$url = "YOUR-URL-HERE"

# Health check
Invoke-RestMethod -Uri "$url/health"

# Metrics
Invoke-RestMethod -Uri "$url/metrics" | Select-String "ingestion_" | Select-Object -First 5

# Test webhook
Invoke-RestMethod -Uri "$url/api/v1/ingest/webhook/freshdesk" -Method Post -Body '{"subject": "Railway Test", "id": 12345}' -ContentType "application/json"
```

## ✅ Success Indicators

After deployment, you should see:

- ✅ Build completed successfully
- ✅ Deployment status: Running
- ✅ Health check: Passing
- ✅ Service URL assigned

## 📊 Monitor Deployment

```powershell
# View logs
railway logs

# Check status
railway status

# Open Railway dashboard
railway open
```

## 🔧 If Something Goes Wrong

### Build Fails

```powershell
railway logs
```

Look for errors in the build output

### Service Crashes

```powershell
railway logs --tail 50
```

Check for database/Redis connection errors

### Environment Variables Missing

```powershell
railway variables
```

Verify all variables are set

## 🎯 After Successful Deployment

1. **Copy your service URL** (from `railway domain`)
2. **Update webhook URLs** in Freshdesk/Zendesk:
   - Freshdesk: `https://your-url/api/v1/ingest/webhook/freshdesk`
   - Zendesk: `https://your-url/api/v1/ingest/webhook/zendesk`
3. **Monitor metrics**: `https://your-url/metrics`
4. **Check logs**: `railway logs --follow`

## 💰 Cost Estimate

Railway free tier: $5/month credit
Expected usage: ~$3-4/month

Monitor in Railway dashboard → Usage

---

**Total Time**: 5-10 minutes
**Difficulty**: Easy (just copy-paste commands)
