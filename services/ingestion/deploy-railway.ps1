# Railway Deployment Script for Ingestion Service

Write-Host "🚀 Deploying Ingestion Service to Railway" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Login
Write-Host "Step 1: Logging in to Railway..." -ForegroundColor Yellow
railway login

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Login failed. Please try again." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Login successful!" -ForegroundColor Green
Write-Host ""

# Step 2: Initialize project
Write-Host "Step 2: Initializing Railway project..." -ForegroundColor Yellow
Write-Host "Please select 'Create a new project' and name it 'aivora-ingestion-service'" -ForegroundColor Cyan
railway init

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Project initialization failed." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Project initialized!" -ForegroundColor Green
Write-Host ""

# Step 3: Set environment variables
Write-Host "Step 3: Setting environment variables..." -ForegroundColor Yellow

$envVars = @{
    "DATABASE_URL"              = "postgresql://neondb_owner:npg_PV8mUupGQMB1@ep-young-snow-a1h4us5d-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    "REDIS_URL"                 = "rediss://default:AWe7AAIncDJjZDNhMDAxMmQzZjY0OTQzOTliYzMyYTViNGUxNWY5ZnAyMjY1NTU@sterling-ant-26555.upstash.io:6379"
    "PORT"                      = "8080"
    "RATE_LIMIT_PER_MINUTE"     = "100"
    "CIRCUIT_BREAKER_THRESHOLD" = "5"
    "CIRCUIT_BREAKER_TIMEOUT"   = "30"
    "FRESHDESK_WEBHOOK_SECRET"  = ""
    "ZENDESK_WEBHOOK_SECRET"    = ""
}

foreach ($key in $envVars.Keys) {
    Write-Host "  Setting $key..." -NoNewline
    railway variables set "$key=$($envVars[$key])" | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
    }
    else {
        Write-Host " ❌" -ForegroundColor Red
    }
}

Write-Host "✅ Environment variables set!" -ForegroundColor Green
Write-Host ""

# Step 4: Deploy
Write-Host "Step 4: Deploying to Railway..." -ForegroundColor Yellow
railway up

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Deployment failed. Check logs with 'railway logs'" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Deployment successful!" -ForegroundColor Green
Write-Host ""

# Step 5: Get service URL
Write-Host "Step 5: Getting service URL..." -ForegroundColor Yellow
$url = railway domain

Write-Host ""
Write-Host "🎉 Deployment Complete!" -ForegroundColor Green
Write-Host "======================" -ForegroundColor Green
Write-Host ""
Write-Host "Service URL: $url" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Test health: curl $url/health" -ForegroundColor White
Write-Host "2. View metrics: curl $url/metrics" -ForegroundColor White
Write-Host "3. View logs: railway logs" -ForegroundColor White
Write-Host "4. Open dashboard: railway open" -ForegroundColor White
Write-Host ""
Write-Host "Configure webhooks:" -ForegroundColor Yellow
Write-Host "Freshdesk: $url/api/v1/ingest/webhook/freshdesk" -ForegroundColor White
Write-Host "Zendesk: $url/api/v1/ingest/webhook/zendesk" -ForegroundColor White
