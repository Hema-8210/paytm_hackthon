# SkillPath Architecture Overview

SkillPath is designed with a decoupled full-stack architecture consisting of a React + TypeScript single-page frontend, a Python FastAPI backend, SQLAlchemy ORM, and an AI service layer for deterministic skill gap analysis and NLP text extraction.

```
                  ┌─────────────────────────────────────┐
                  │          React + TS Frontend        │
                  │   Tailwind CSS / Recharts / Vite    │
                  └──────────────────┬──────────────────┘
                                     │ REST APIs (JWT)
                  ┌──────────────────▼──────────────────┐
                  │          FastAPI Backend            │
                  │   API Routers & Auth Dependency     │
                  └──────────┬──────────────────┬───────┘
                             │                  │
        ┌────────────────────▼─────┐      ┌─────▼────────────────────┐
        │     AI Service Layer     │      │   SQLAlchemy ORM Engine  │
        │  PyMuPDF / TF-IDF NLP    │      │ PostgreSQL / SQLite DB   │
        │ Skill Gap Engine / LLM   │      └──────────────────────────┘
        └──────────────────────────┘
```

## Core Modules

1. **Frontend Layer (`frontend/src/`)**:
   - Component architecture separating pages (`LandingPage`, `DashboardPage`, `ResumeAnalyzerPage`, `JobAnalyzerPage`, `SkillGapPage`, `ProjectLibraryPage`, `RoadmapPage`, `ProgressPage`) from layout and UI widgets.
   - API client module (`api.ts`) managing JWT auth headers and error handling.

2. **Backend API Layer (`backend/app/api/`)**:
   - Modular routers: `auth`, `users`, `skills`, `jobs`, `resume`, `skill_gap`, `projects`, `roadmaps`, `progress`, `assistant`.
   - Security: Password hashing with bcrypt, JWT token validation dependencies (`deps.py`).

3. **AI/NLP Layer (`backend/app/ai/`)**:
   - `embeddings.py`: TF-IDF vector cosine similarity and alias normalization dictionary (`ReactJS` -> `React`, `JS` -> `JavaScript`).
   - `skill_extractor.py`: Tokenization, regex, and n-gram extraction for resumes and job descriptions.
   - `resume_analyzer.py`: PDF document parsing using PyMuPDF (`fitz`), section extraction, and confidence scoring (e.g. Python 96%, SQL 91%).
   - `job_analyzer.py`: Processes raw job descriptions into structured requirement profiles.
   - `skill_gap_engine.py`: Computes requirement match % and priority scores (`gap * importance`).
   - `project_recommender.py`: Ranks database projects by missing skill coverage.
   - `roadmap_generator.py`: Generates 5-phase structured learning roadmaps validated against database skill graph.
   - `llm_client.py`: OpenAI client with smart local NLP fallback engine.
