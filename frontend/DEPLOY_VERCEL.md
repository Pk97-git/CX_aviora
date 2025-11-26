# Aivora Frontend - Vercel Deployment Guide

## Prerequisites

1. Vercel account (sign up at https://vercel.com)
2. GitHub repository with frontend code
3. Intelligence Service deployed and accessible

## Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Connect Repository**

   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Select the `frontend` directory as the root

2. **Configure Build Settings**

   - Framework Preset: **Vite**
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

3. **Set Environment Variables**

   ```
   VITE_API_BASE_URL=https://aivora-intelligence.onrender.com
   VITE_WS_URL=wss://aivora-intelligence.onrender.com/ws
   ```

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (~2-3 minutes)
   - Your app will be live at `https://your-project.vercel.app`

### Option 2: Deploy via Vercel CLI

```powershell
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend directory
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel --prod

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? [Your account]
# - Link to existing project? No
# - Project name? aivora-frontend
# - Directory? ./
# - Override settings? No
```

### Option 3: Deploy to Netlify

1. **Install Netlify CLI**

   ```powershell
   npm install -g netlify-cli
   ```

2. **Build the project**

   ```powershell
   cd frontend
   npm run build
   ```

3. **Deploy**

   ```powershell
   netlify deploy --prod --dir=dist
   ```

4. **Set Environment Variables** (via Netlify Dashboard)
   - Go to Site settings > Environment variables
   - Add:
     - `VITE_API_BASE_URL`: Your Intelligence Service URL
     - `VITE_WS_URL`: WebSocket URL

## Post-Deployment

### 1. Update CORS in Intelligence Service

Add your Vercel domain to the CORS allowed origins in `services/intelligence/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-project.vercel.app",  # Add this
        "https://*.vercel.app",             # Or use wildcard
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Verify Deployment

1. Visit your Vercel URL
2. Open browser DevTools > Network tab
3. Navigate to Dashboard
4. Verify API calls to Intelligence Service are successful
5. Check for CORS errors (should be none)

### 3. Custom Domain (Optional)

1. Go to Vercel Dashboard > Your Project > Settings > Domains
2. Add your custom domain (e.g., `app.aivora.com`)
3. Update DNS records as instructed
4. Update CORS origins in backend

## Troubleshooting

### Build Fails

- Check `package.json` dependencies are correct
- Ensure `vite.config.ts` is properly configured
- Review build logs in Vercel dashboard

### API Calls Fail

- Verify `VITE_API_BASE_URL` environment variable is set
- Check Intelligence Service is running and accessible
- Verify CORS is configured correctly in backend

### Blank Page

- Check browser console for errors
- Verify `dist/index.html` exists after build
- Check Vercel deployment logs

## Continuous Deployment

Vercel automatically deploys on every push to `main` branch:

- **Production**: Pushes to `main` → `your-project.vercel.app`
- **Preview**: Pull requests → `pr-123.your-project.vercel.app`

## Performance Optimization

1. **Enable Caching**

   - Vercel automatically caches static assets
   - Configure in `vercel.json` if needed

2. **Enable Compression**

   - Gzip/Brotli enabled by default

3. **Analytics**
   - Enable Vercel Analytics in dashboard
   - Monitor Core Web Vitals

## Cost

- **Hobby Plan**: Free

  - 100GB bandwidth/month
  - Unlimited deployments
  - Perfect for development/demo

- **Pro Plan**: $20/month
  - 1TB bandwidth
  - Team collaboration
  - Custom domains
