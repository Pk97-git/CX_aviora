# Production Features Test Script

Write-Host "🧪 Testing Production Features" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

$baseUrl = "http://localhost:8080"

# Test 1: Prometheus Metrics
Write-Host "1. Testing Prometheus Metrics..." -NoNewline
try {
    $metrics = Invoke-RestMethod -Uri "$baseUrl/metrics" -Method Get
    if ($metrics -match "ingestion_http_requests_total") {
        Write-Host " ✅ PASS" -ForegroundColor Green
    }
    else {
        Write-Host " ❌ FAIL (metrics not found)" -ForegroundColor Red
    }
}
catch {
    Write-Host " ❌ FAIL" -ForegroundColor Red
}

# Test 2: Idempotency
Write-Host "2. Testing Idempotency..." -NoNewline
$payload = '{"subject": "Idempotency Test", "description": "Same ticket", "email": "idempotent@test.com", "priority": 2, "status": 2, "id": 88888}'

try {
    $response1 = Invoke-RestMethod -Uri "$baseUrl/api/v1/ingest/webhook/freshdesk" -Method Post -Body $payload -ContentType "application/json"
    $ticketId1 = $response1.ticket_id
    
    Start-Sleep -Seconds 1
    
    $response2 = Invoke-RestMethod -Uri "$baseUrl/api/v1/ingest/webhook/freshdesk" -Method Post -Body $payload -ContentType "application/json"
    $ticketId2 = $response2.ticket_id
    
    if ($ticketId1 -eq $ticketId2 -and $response2.status -eq "already_exists") {
        Write-Host " ✅ PASS (same ticket ID: $ticketId1)" -ForegroundColor Green
    }
    else {
        Write-Host " ❌ FAIL (different IDs or wrong status)" -ForegroundColor Red
    }
}
catch {
    Write-Host " ❌ FAIL" -ForegroundColor Red
}

# Test 3: Rate Limiting
Write-Host "3. Testing Rate Limiting (10 req/min)..." -NoNewline
$rateLimitHit = $false
try {
    for ($i = 1; $i -le 15; $i++) {
        try {
            $null = Invoke-RestMethod -Uri "$baseUrl/health" -Method Get -ErrorAction Stop
        }
        catch {
            if ($_.Exception.Response.StatusCode.value__ -eq 429) {
                $rateLimitHit = $true
                break
            }
        }
        Start-Sleep -Milliseconds 100
    }
    
    if ($rateLimitHit) {
        Write-Host " ✅ PASS (rate limit enforced)" -ForegroundColor Green
    }
    else {
        Write-Host " ⚠️  WARN (rate limit not hit, may need more requests)" -ForegroundColor Yellow
    }
}
catch {
    Write-Host " ❌ FAIL" -ForegroundColor Red
}

# Test 4: Circuit Breaker (simulated - just verify it exists in metrics)
Write-Host "4. Testing Circuit Breaker Metrics..." -NoNewline
try {
    $metrics = Invoke-RestMethod -Uri "$baseUrl/metrics" -Method Get
    if ($metrics -match "ingestion_circuit_breaker_state") {
        Write-Host " ✅ PASS (circuit breaker initialized)" -ForegroundColor Green
    }
    else {
        Write-Host " ❌ FAIL (circuit breaker metrics not found)" -ForegroundColor Red
    }
}
catch {
    Write-Host " ❌ FAIL" -ForegroundColor Red
}

# Test 5: Webhook Signature Validation (dev mode - should pass without signature)
Write-Host "5. Testing Webhook Auth (dev mode)..." -NoNewline
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/v1/ingest/webhook/freshdesk" -Method Post -Body '{"subject": "Auth Test", "id": 99999}' -ContentType "application/json"
    if ($response.status -eq "received" -or $response.status -eq "already_exists") {
        Write-Host " ✅ PASS (dev mode allows requests)" -ForegroundColor Green
    }
    else {
        Write-Host " ❌ FAIL" -ForegroundColor Red
    }
}
catch {
    Write-Host " ❌ FAIL" -ForegroundColor Red
}

# Test 6: Database Metrics
Write-Host "6. Testing Database Metrics..." -NoNewline
try {
    $metrics = Invoke-RestMethod -Uri "$baseUrl/metrics" -Method Get
    if ($metrics -match "ingestion_db_operations_total") {
        Write-Host " ✅ PASS" -ForegroundColor Green
    }
    else {
        Write-Host " ❌ FAIL" -ForegroundColor Red
    }
}
catch {
    Write-Host " ❌ FAIL" -ForegroundColor Red
}

# Test 7: Redis Metrics
Write-Host "7. Testing Redis Metrics..." -NoNewline
try {
    $metrics = Invoke-RestMethod -Uri "$baseUrl/metrics" -Method Get
    if ($metrics -match "ingestion_redis_operations_total") {
        Write-Host " ✅ PASS" -ForegroundColor Green
    }
    else {
        Write-Host " ❌ FAIL" -ForegroundColor Red
    }
}
catch {
    Write-Host " ❌ FAIL" -ForegroundColor Red
}

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "✨ Production Features Test Complete!" -ForegroundColor Cyan
