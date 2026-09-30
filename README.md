# SkillPath — Full-Stack AI Career Skill Gap Platform

> **Tagline:** Turn your career goal into a path you can actually follow.

SkillPath is a full-stack, production-quality web application designed to help students and developers bridge the gap between their current skills and real job requirements.

---

## 🌟 Core Product Loop

```
JOB → SKILLS → GAP → PROJECT → LEARNING → PROGRESS
```

1. **Upload Resume**: PDF parsing with PyMuPDF & NLP skill extraction confidence scores.
2. **Select Target Role / Analyze Job**: Compare profile against target role benchmarks or custom pasted job posts.
3. **Skill Gap Engine**: Calculate deterministic Requirement Match Score %, gap levels, and priorities.
4. **Project Recommendations**: Matched portfolio projects with step-by-step implementation guides.
5. **AI Learning Roadmap**: 5-phase structured learning path mapped to database skills.
6. **Progress Tracking**: Real-time progress updates, streak monitoring, and gap countdowns.
7. **AI Career Assistant**: Context-aware floating chatbot utilizing current user state.

---

## 🛠️ Technology Stack

- **Frontend**: React.js 19, TypeScript, Tailwind CSS v4, React Router v7, Recharts, Lucide Icons, Vite.
- **Backend**: Python 3.11/3.14, FastAPI, Pydantic v2, SQLAlchemy ORM.
- **Database**: PostgreSQL (Production) / SQLite (Development).
- **AI & NLP**: spaCy / scikit-learn (TF-IDF vector similarity), PyMuPDF (`fitz`), OpenAI API integration with deterministic local NLP fallback.
- **Authentication**: JWT authentication with bcrypt password hashing.

---

## 🚀 Quick Start & Installation

### Prerequisites
- Python 3.10+
- Node.js v20+ & npm
- Docker (optional)

### 1. Setup Backend
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt

# Run FastAPI backend (Auto-creates and seeds DB on startup)
uvicorn app.main:app --reload --port 8000
```
Backend API will be available at `http://localhost:8000` (Swagger docs at `http://localhost:8000/api/docs`).

### 2. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend application will run at `http://localhost:5173`.

---

## 🔑 Demo Login Credentials

The application automatically seeds a demo account on startup:
- **Email**: `demo@skillpath.dev`
- **Password**: `password123`

---

## 🐳 Docker Deployment

To run the complete full-stack environment with PostgreSQL using Docker Compose:

```bash
docker-compose up --build
```
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

---

## 🧪 Testing

Run backend unit tests:
```bash
cd backend
$env:PYTHONPATH="."  # Windows PowerShell
.\venv\Scripts\pytest app/tests/test_api.py
```

Run frontend build verification:
```bash
cd frontend
npm run build
```

---

## 📁 Project Structure

```
skillpath/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI REST endpoint routers
│   │   ├── ai/              # NLP, TF-IDF, PyMuPDF & LLM service layer
│   │   ├── core/            # Config & Security JWT helpers
│   │   ├── database/        # SQLAlchemy session & seed script
│   │   ├── models/          # Database ORM models
│   │   ├── schemas/         # Pydantic validation schemas
│   │   ├── tests/           # Backend unit tests
│   │   └── main.py          # FastAPI application entry point
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/      # React UI components (CircularProgress, CareerAssistantWidget, etc.)
│   │   ├── pages/           # Landing, Dashboard, Resume, Job, SkillGap, Projects, Roadmap, Progress
│   │   ├── services/        # Typed API service client
│   │   ├── App.tsx          # Router layout & auth state
│   │   └── index.css        # Tailwind CSS configuration
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── docs/                    # Architecture, API & Database documentation
├── docker-compose.yml
├── .env.example
└── README.md
```
