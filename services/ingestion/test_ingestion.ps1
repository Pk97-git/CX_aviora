$baseUrl = "http://localhost:8080"

function Test-Endpoint {
    param (
        [string]$Name,
        [string]$Uri,
        [string]$Method = "GET",
        [string]$Body = "",
        [int]$ExpectedStatus = 200
    )

    Write-Host "Testing $Name..." -NoNewline
    try {
        $params = @{
            Uri         = "$baseUrl$Uri"
            Method      = $Method
            ErrorAction = "Stop"
        }
        if ($Body) {
            $params.Body = $Body
            $params.ContentType = "application/json"
        }

        $response = Invoke-RestMethod @params
        Write-Host " ✅ OK" -ForegroundColor Green
        # Write-Host ($response | ConvertTo-Json -Depth 2)
    }
    catch {
        $status = $_.Exception.Response.StatusCode.value__
        if ($status -eq $ExpectedStatus) {
            Write-Host " ✅ OK (Expected $status)" -ForegroundColor Green
        }
        else {
            Write-Host " ❌ FAILED (Got $status, Expected $ExpectedStatus)" -ForegroundColor Red
            Write-Host $_.Exception.Message
        }
    }
}

# 1. Health Check
Test-Endpoint -Name "Health Check" -Uri "/health"

# 2. Freshdesk Webhook (Valid)
$fdPayload = '{
    "subject": "Docker Test Ticket",
    "description": "Testing from Docker container",
    "email": "docker@test.com",
    "priority": 4,
    "status": 2,
    "id": 999
}'
Test-Endpoint -Name "Freshdesk Webhook (Valid)" -Uri "/api/v1/ingest/webhook/freshdesk" -Method "POST" -Body $fdPayload

# 3. Zendesk Webhook (Valid)
$zdPayload = '{
    "ticket": {
        "id": 888,
        "subject": "Zendesk Docker Test",
        "description": "Testing ZD from Docker",
        "priority": "urgent",
        "status": "new",
        "requester": {
            "name": "Docker User",
            "email": "docker@zendesk.com"
        }
    }
}'
Test-Endpoint -Name "Zendesk Webhook (Valid)" -Uri "/api/v1/ingest/webhook/zendesk" -Method "POST" -Body $zdPayload

# 4. Invalid JSON
Test-Endpoint -Name "Invalid JSON" -Uri "/api/v1/ingest/webhook/freshdesk" -Method "POST" -Body '{invalid}' -ExpectedStatus 400

# 5. Empty Payload (Should fail validation or normalization)
# Currently normalization might succeed with empty fields, but let's check if it crashes
Test-Endpoint -Name "Empty Payload" -Uri "/api/v1/ingest/webhook/freshdesk" -Method "POST" -Body '{}' -ExpectedStatus 200 

Write-Host "`nTests Completed."
