from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import User, TargetRole, JobRequirement, Skill, UserSkill
from app.schemas.schemas import SkillGapResponse
from app.api.deps import get_current_user
from app.ai.skill_gap_engine import calculate_skill_gap

router = APIRouter(prefix="/skill-gap", tags=["Skill Gap Engine"])

@router.get("", response_model=SkillGapResponse)
def get_current_skill_gap(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    target_role_id = current_user.target_role_id
    if not target_role_id:
        # Default to first role (Data Analyst / Software Engineer) if user hasn't set one yet
        first_role = db.query(TargetRole).first()
        if first_role:
            target_role_id = first_role.id
        else:
            raise HTTPException(status_code=400, detail="No target role selected yet. Please complete onboarding or select a target role.")
            
    role = db.query(TargetRole).filter(TargetRole.id == target_role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Target role not found.")
        
    # Get target role job requirements
    job_reqs = db.query(JobRequirement).filter(JobRequirement.target_role_id == role.id).all()
    
    formatted_job_reqs = []
    for jr in job_reqs:
        formatted_job_reqs.append({
            "skill_id": jr.skill_id,
            "name": jr.skill.name,
            "category": jr.skill.category,
            "required_level": jr.required_level,
            "importance": jr.importance,
            "frequency": jr.frequency
        })
        
    # Get current user's skills
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == current_user.id).all()
    formatted_user_skills = []
    for us in user_skills:
        formatted_user_skills.append({
            "skill_id": us.skill_id,
            "name": us.skill.name,
            "proficiency_level": us.proficiency_level
        })
        
    gap_result = calculate_skill_gap(formatted_user_skills, formatted_job_reqs, role.title)
    return gap_result
