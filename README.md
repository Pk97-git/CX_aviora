# Aivora - AI-First CX Operations Cloud

## 🚀 Overview
Aivora is a universal CX operations platform that orchestrates workflows between frontline tools (Freshdesk, Zendesk) and internal ops tools (ERP, JIRA, Finance). It uses AI to understand, classify, and route tickets, enforcing policy-based governance and providing predictive insights.

## 🛠️ Tech Stack
- **Backend**: Go (Ingestion, Orchestration), Python (AI/ML)
- **Frontend**: React 18, TypeScript, Tailwind CSS
- **Database**: PostgreSQL, Redis, MongoDB
- **AI/ML**: OpenAI/Groq, PyTorch, Hugging Face
- **Infrastructure**: Docker, Kubernetes (EKS), Terraform

## 🏗️ Project Structure
```
aivora/
├── services/           # Microservices
│   ├── ingestion/      # Ticket ingestion (Go)
│   ├── intelligence/   # AI/ML analysis (Python)
│   ├── orchestration/  # Workflow engine (Go)
│   └── ...
├── frontend/           # React application
├── infrastructure/     # Docker & Terraform configs
└── docs/               # Documentation
```

## 🚦 Getting Started

### Prerequisites
- Git
- Docker Desktop
- Go 1.21+
- Python 3.11+
- Node.js 18+

### Local Development
1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/aivora.git
   cd aivora
   ```

2. Start infrastructure
   ```bash
   cd infrastructure/docker
   docker-compose up -d
   ```

3. Run services (see individual service READMEs)

## 📚 Documentation
- [Architecture Overview](docs/architecture.md)
- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)
