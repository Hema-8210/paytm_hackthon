# SkillPath API Documentation

Base URL: `/api`

## Authentication

- `POST /api/auth/register` — Register a new user (`name`, `email`, `password`). Returns JWT access token.
- `POST /api/auth/login` — Authenticate existing user (`email`, `password`). Returns JWT access token.
- `GET /api/auth/me` — Fetch current user profile (requires `Authorization: Bearer <token>`).

## Users & Onboarding

- `POST /api/users/onboarding` — Update education, target role, and select current skills.

## Skills & Roles

- `GET /api/skills` — List skills (optional `category` or `search` query parameters).
- `GET /api/jobs/roles` — Fetch supported target roles.
- `POST /api/jobs/analyze` — Process raw job description text into structured skill requirements.

## Resume Analyzer

- `POST /api/resume/upload` — Upload PDF resume (max 10MB). Returns extracted skills and confidence percentages.
- `POST /api/resume/confirm-skills` — Save confirmed extracted skills to user database profile.

## Skill Gap Engine

- `GET /api/skill-gap` — Compute Requirement Match Score %, skill coverage matrix, top gaps, and recommended next step.

## Projects & Recommendations

- `GET /api/projects` — List available projects (optional `category`, `difficulty`, `search`).
- `GET /api/projects/recommendations` — Fetch projects tailored to close user's current high-priority skill gaps.
- `GET /api/projects/{id}` — Fetch detailed project view with implementation steps.

## Learning Roadmap

- `GET /api/roadmaps/current` — Fetch active 5-phase learning roadmap.
- `POST /api/roadmaps/generate` — Generate or regenerate personalized roadmap.
- `PUT /api/roadmaps/steps/{step_id}/status` — Update step status (`not_started`, `in_progress`, `completed`).

## Progress & Assistant

- `GET /api/progress` — Fetch overall progress metrics (roadmap completion %, projects built, active streak).
- `POST /api/assistant/chat` — Context-aware AI career assistant chat endpoint.
