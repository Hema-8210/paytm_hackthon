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

## 🛠️ Technology Stack & Architecture

- **Frontend**: React.js 19, TypeScript, Tailwind CSS v4, React Router v7, Recharts, Lucide Icons, Vite.
- **Backend**: Python 3.14/3.11, FastAPI, Pydantic v2, SQLAlchemy ORM, Alembic Migrations.
- **Database**: PostgreSQL (Supabase / Production) / SQLite (Development).
- **AI & NLP**: spaCy / scikit-learn (TF-IDF vector similarity), PyMuPDF (`fitz`), OpenAI API integration with deterministic local NLP fallback (`ai_provider.py`).
- **Authentication**: JWT authentication with bcrypt password hashing.

---

## 🔐 Verified Hackathon & Test Account

- **Name**: `SkillPath Demo User`
- **Email**: `demo@skillpath.app`
- **Password**: `Password123!`

Alternative seeded account:
- **Email**: `demo@skillpath.dev`
- **Password**: `password123`

---

## 🚀 Public Cloud Deployment Guide

### 1. Deploy Frontend (Vercel)
- **Root Directory**: `frontend/`
- **Framework Preset**: `Vite`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Environment Variable**: `VITE_API_URL=https://skillpath-api.onrender.com`

### 2. Deploy Backend (Render Web Service)
- **Root Directory**: `backend/`
- **Build Command**: `pip install -r requirements.txt && alembic upgrade head`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health Check Path**: `/health`
- **Environment Variables**:
  - `DATABASE_URL=postgresql://user:pass@host:5432/dbname`
  - `JWT_SECRET=production-secure-random-secret-2026`
  - `OPENAI_API_KEY=your_openai_key`
  - `FRONTEND_URL=https://skillpath.vercel.app`

### 3. Database & Storage (Supabase)
- **Database**: Supabase PostgreSQL with Alembic migration running `alembic upgrade head`.
- **Storage**: Supabase Storage bucket `skillpath-resumes` for private PDF resume uploads.

---

## 🐳 Docker Local Setup

To run locally with Docker:
```bash
docker-compose up -d --build
```
- Frontend: `http://localhost:5173`
- Backend API Docs: `http://localhost:8000/api/docs`
- Healthcheck: `http://localhost:8000/health`
