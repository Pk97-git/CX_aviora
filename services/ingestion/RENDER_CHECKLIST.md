# Render Deployment - Step-by-Step Checklist

## ✅ Pre-Deployment (Already Done)

- [x] Code pushed to GitHub: https://github.com/Pk97-git/CX_aviora
- [x] Railway configuration files created
- [x] All production features implemented

---

## 🚀 Deployment Steps (Follow in Order)

### Step 1: Sign Up for Render

- [ ] Go to https://render.com
- [ ] Click "Get Started for Free"
- [ ] Choose "Sign up with GitHub"
- [ ] Authorize Render to access your GitHub

### Step 2: Create New Web Service

- [ ] Click "New +" button (top right)
- [ ] Select "Web Service"
- [ ] Find and select repository: **CX_aviora**
- [ ] Click "Connect"

### Step 3: Configure Basic Settings

**Name:**

```
aivora-ingestion-service
```

**Region:**

```
Singapore
```

**Branch:**

```
main
```

**Root Directory:**

```
services/ingestion
```

**Runtime:**

```
Go
```

### Step 4: Configure Build Settings

**Build Command:**

```
go build -o ingestion-service ./cmd/server
```

**Start Command:**

```
./ingestion-service
```

### Step 5: Select Plan

- [ ] Choose **Free** instance type

### Step 6: Add Environment Variables

Click "Advanced" → "Add Environment Variable"

**Copy-paste these one by one:**

**Variable 1:**

```
Name: DATABASE_URL
Value: postgresql://neondb_owner:npg_PV8mUupGQMB1@ep-young-snow-a1h4us5d-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

**Variable 2:**

```
Name: REDIS_URL
Value: rediss://default:AWe7AAIncDJjZDNhMDAxMmQzZjY0OTQzOTliYzMyYTViNGUxNWY5ZnAyMjY1NTU@sterling-ant-26555.upstash.io:6379
```

**Variable 3:**

```
Name: PORT
Value: 10000
```

**Variable 4:**

```
Name: RATE_LIMIT_PER_MINUTE
Value: 100
```

**Variable 5:**

```
Name: CIRCUIT_BREAKER_THRESHOLD
Value: 5
```

**Variable 6:**

```
Name: CIRCUIT_BREAKER_TIMEOUT
Value: 30
```

**Variable 7:**

```
Name: FRESHDESK_WEBHOOK_SECRET
Value: (leave empty)
```

**Variable 8:**

```
Name: ZENDESK_WEBHOOK_SECRET
Value: (leave empty)
```

### Step 7: Configure Health Check

**Health Check Path:**

```
/health
```

**Health Check Timeout:**

```
30
```

### Step 8: Deploy

- [ ] Click "Create Web Service"
- [ ] Wait for build to complete (~3-5 minutes)
- [ ] Watch the logs for any errors

---

## 🧪 After Deployment

### Your Service URL

```
https://aivora-ingestion-service.onrender.com
```

### Test Commands

**Health Check:**

```powershell
Invoke-RestMethod -Uri "https://aivora-ingestion-service.onrender.com/health"
```

**Expected Response:**

```json
{
  "status": "ok",
  "service": "ingestion"
}
```

**Metrics:**

```powershell
Invoke-RestMethod -Uri "https://aivora-ingestion-service.onrender.com/metrics" | Select-String "ingestion_" | Select-Object -First 10
```

**Test Webhook:**

```powershell
Invoke-RestMethod -Uri "https://aivora-ingestion-service.onrender.com/api/v1/ingest/webhook/freshdesk" -Method Post -Body '{"subject": "Render Test", "description": "Testing deployment", "id": 99999}' -ContentType "application/json"
```

---

## ✅ Success Indicators

After deployment completes, verify:

- [ ] Build status: "Live" (green)
- [ ] Health check: Passing
- [ ] Logs show: "👂 Listening on port 10000..."
- [ ] Logs show: "✅ Successfully connected to Redis"
- [ ] Logs show: "✅ Database Schema Verified"
- [ ] Health endpoint returns 200 OK
- [ ] Metrics endpoint accessible

---

## 📊 Monitor Your Service

**View Logs:**

- Render Dashboard → Your Service → Logs tab
- Real-time streaming

**View Metrics:**

- Render Dashboard → Your Service → Metrics tab
- CPU, Memory, Network usage

**Manual Redeploy:**

- Render Dashboard → Your Service → Manual Deploy button

---

## 🔄 Auto-Deploy Enabled

Every push to `main` branch will automatically deploy:

```powershell
git add .
git commit -m "Update service"
git push origin main
# Render automatically builds and deploys
```

---

## ⚠️ Important Notes

1. **First Request Delay**: Free tier sleeps after 15 min inactivity

   - First request after sleep: ~30 seconds
   - Solution: Set up cron job at cron-job.org

2. **Port**: Render uses 10000, not 8080

   - Our service reads from PORT env var ✅

3. **SSL**: Automatic HTTPS with free SSL certificate ✅

---

## 🎯 Next Steps After Deployment

1. **Test all endpoints** (commands above)
2. **Configure webhooks** in Freshdesk/Zendesk:
   - Freshdesk: `https://aivora-ingestion-service.onrender.com/api/v1/ingest/webhook/freshdesk`
   - Zendesk: `https://aivora-ingestion-service.onrender.com/api/v1/ingest/webhook/zendesk`
3. **Set up cron job** to keep service awake (optional)
4. **Monitor logs** for first few hours

---

**Estimated Time**: 10 minutes
**Cost**: $0/month (Free tier)
**Auto-Deploy**: ✅ Enabled
