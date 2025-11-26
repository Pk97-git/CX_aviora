# Deploy script for Vercel
Write-Host "🚀 Deploying Aivora Frontend to Vercel..." -ForegroundColor Cyan

# Check if vercel CLI is installed
if (-not (Get-Command vercel -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Vercel CLI not found. Installing..." -ForegroundColor Yellow
    npm install -g vercel
}

# Navigate to frontend directory
Set-Location -Path $PSScriptRoot

# Build the project
Write-Host "📦 Building project..." -ForegroundColor Cyan
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Build successful!" -ForegroundColor Green

# Deploy to Vercel
Write-Host "🌐 Deploying to Vercel..." -ForegroundColor Cyan
vercel --prod

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Deployment successful!" -ForegroundColor Green
    Write-Host "🎉 Your app is now live!" -ForegroundColor Cyan
}
else {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    exit 1
}
