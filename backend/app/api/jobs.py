from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.models import TargetRole, Skill, JobRequirement
from app.schemas.schemas import TargetRoleOut, JobAnalysisRequest, JobAnalysisResponse
from app.ai.job_analyzer import analyze_job_description_text

router = APIRouter(prefix="/jobs", tags=["Jobs & Roles"])

@router.get("/roles", response_model=List[TargetRoleOut])
def get_target_roles(db: Session = Depends(get_db)):
    return db.query(TargetRole).all()

@router.post("/analyze", response_model=JobAnalysisResponse)
def analyze_job_description(payload: JobAnalysisRequest, db: Session = Depends(get_db)):
    job_title = payload.job_title or "Target Job"
    if payload.target_role_id:
        role = db.query(TargetRole).filter(TargetRole.id == payload.target_role_id).first()
        if role:
            job_title = role.title

    try:
        result = analyze_job_description_text(payload.job_description, job_title)
        
        # Attach matching database skill IDs if they exist
        for skill_item in result["skills"]:
            existing_sk = db.query(Skill).filter(Skill.name.ilike(skill_item["name"])).first()
            if existing_sk:
                skill_item["skill_id"] = existing_sk.id

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to analyze job description: {str(e)}")
