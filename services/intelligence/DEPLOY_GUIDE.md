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

## 3. Environment Variables

Copy these values from your local `.env` or the list below:

| Key              | Value                                                   |
| ---------------- | ------------------------------------------------------- |
| `DATABASE_URL`   | `<your-neon-database-url>` (Get from Neon dashboard)    |
| `REDIS_URL`      | `<your-upstash-redis-url>` (Get from Upstash dashboard) |
| `GROQ_API_KEY`   | `<your-groq-api-key>` (Get from Groq console)           |
| `PYTHON_VERSION` | `3.11.9`                                                |

## 4. Deploy

- Click **Create Web Service**.
- Wait for the build to finish.
- Once live, you will get a URL like `https://aivora-intelligence-service.onrender.com`.

## 5. Verification

- Visit `/health` endpoint: `https://aivora-intelligence-service.onrender.com/health`
- Send a test webhook to the **Ingestion Service** and check the **Intelligence Service** logs.
