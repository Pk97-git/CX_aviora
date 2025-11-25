# 🚀 Deploying Intelligence Service to Render

## 1. Create New Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** -> **Web Service**.
3. Select your repository: `Pk97-git/CX_aviora`.
4. Click **Connect**.

## 2. Configure Service

- **Name**: `aivora-intelligence-service`
- **Region**: Singapore (same as Ingestion)
- **Branch**: `main`
- **Root Directory**: `services/intelligence`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Instance Type**: Free
- Once live, you will get a URL like `https://aivora-intelligence-service.onrender.com`.

## 5. Verification

- Visit `/health` endpoint: `https://aivora-intelligence-service.onrender.com/health`
- Send a test webhook to the **Ingestion Service** and check the **Intelligence Service** logs.
