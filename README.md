# Aivora - AI-First CX Operations Platform

## 🚀 Overview

AI-powered customer support platform with multi-tenancy, intelligent ticket analysis, and external system integrations (Freshdesk, JIRA, Slack).

## ✅ Current Status: Phase 1-3 Complete (43%)

**Live Features:**

- ✅ Multi-tenant architecture with RBAC
- ✅ JWT authentication
- ✅ AI-powered ticket understanding (Groq LLM)
- ✅ Webhook ingestion (Freshdesk, Zendesk)
- ✅ External integrations (Freshdesk, JIRA, Slack)
- ✅ Admin dashboard
- ✅ Ticket management UI

## 🛠️ Tech Stack

**Backend:**

- FastAPI (Python 3.11+)
- PostgreSQL (Neon)
- SQLAlchemy (async)
- Groq AI (llama-3.1-70b-versatile)
- JWT authentication

**Frontend:**

- React 18 + Vite
- TypeScript
- Tailwind CSS + Shadcn UI
- Axios

**Integrations:**

- Freshdesk API v2
- JIRA Cloud API v3
- Slack Web API

## 🏗️ Project Structure

```
aivora/
├── services/
│   └── intelligence/          # FastAPI backend
│       ├── app/
│       │   ├── api/routes/   # API endpoints
│       │   ├── models/       # SQLAlchemy models
│       │   ├── integrations/ # External system integrations
│       │   ├── services/     # Business logic
│       │   └── core/         # Auth, database, config
│       ├── migrations/       # Database migrations
│       ├── init_fresh_database.sql  # Fresh DB setup
│       └── requirements.txt
├── frontend/                  # React application
│   ├── src/
│   │   ├── pages/           # Page components
│   │   ├── components/      # Reusable components
│   │   └── lib/             # API clients, utilities
│   └── package.json
├── docker-compose.yml        # Local development
└── README.md
```

## 🚦 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL database (or use Neon)
- Groq API key

### 1. Backend Setup

```bash
cd services/intelligence

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_fresh_database.py

# Start server
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### 3. Access Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 4. Login Credentials

**Password for all users**: `password123`

**TechStart Inc** (SaaS Startup):

- Admin: `sarah.chen@techstart.io`
- Manager: `mike.rodriguez@techstart.io`

**RetailPro Solutions** (E-commerce):

- Admin: `admin@retailpro.com`
- Manager: `carlos.martinez@retailpro.com`

**CloudBase** (Cloud Infrastructure):

- Admin: `admin@cloudbase.io`
- Manager: `priya.patel@cloudbase.io`

## 🐳 Docker Deployment

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

See [DOCKER_GUIDE.md](DOCKER_GUIDE.md) for detailed Docker instructions.

## 📊 Sample Data

The database comes pre-populated with realistic production-like data:

- **3 Companies**: TechStart, RetailPro, CloudBase
- **11 Users**: Admins, managers, agents
- **12 Tickets**: Varied scenarios (refunds, bugs, features, shipping issues)
- **8 Comments**: Customer replies + internal notes
- **7 Integrations**: Freshdesk, Zendesk, Slack, JIRA

All tickets include complete AI analysis:

- Summary, intent, sentiment
- Extracted entities (order IDs, amounts, products)
- AI-suggested priority and category
- Suggested actions with confidence scores

## 🔑 Environment Variables

Create `.env` file in `services/intelligence/`:

```env
DATABASE_URL=postgresql://user:pass@host:5432/dbname
GROQ_API_KEY=your_groq_api_key
JWT_SECRET_KEY=your_secret_key
REDIS_URL=redis://localhost:6379
```

## 📚 API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 Roadmap

- [x] **Phase 1**: Multi-Tenancy & Admin (100%)
- [x] **Phase 2**: Ticket System with AI (100%)
- [x] **Phase 3**: Integrations (100%)
- [ ] **Phase 4**: Workflow Automation
- [ ] **Phase 5**: Task Management
- [ ] **Phase 6**: Policy Engine
- [ ] **Phase 7**: Testing & Polish

## 📝 License

Proprietary - All rights reserved

## 🤝 Contributing

This is a private project. Contact the team for contribution guidelines.
