import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.session import engine, Base, SessionLocal
from app.database.seed import seed_database
from app.api import auth, users, skills, jobs, resume, skill_gap, projects, roadmaps, progress, assistant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("skillpath")

# Create tables
Base.metadata.create_all(bind=engine)

# Auto Seed (Idempotent)
db = SessionLocal()
try:
    seed_database(db)
finally:
    db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Health Check Endpoint (Unauthenticated for Render / Deployment monitor)
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "skillpath-api"}

# CORS Configuration
origins = [
    settings.FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]
if settings.ENVIRONMENT == "production" and settings.FRONTEND_URL:
    # Ensure frontend URL is in origins
    if settings.FRONTEND_URL not in origins:
        origins.append(settings.FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if settings.ENVIRONMENT == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(skills.router, prefix=settings.API_V1_STR)
app.include_router(jobs.router, prefix=settings.API_V1_STR)
app.include_router(resume.router, prefix=settings.API_V1_STR)
app.include_router(skill_gap.router, prefix=settings.API_V1_STR)
app.include_router(projects.router, prefix=settings.API_V1_STR)
app.include_router(roadmaps.router, prefix=settings.API_V1_STR)
app.include_router(progress.router, prefix=settings.API_V1_STR)
app.include_router(assistant.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "message": "Welcome to SkillPath API",
        "tagline": "Turn your career goal into a path you can actually follow.",
        "docs": f"{settings.API_V1_STR}/docs",
        "health": "/health"
    }
