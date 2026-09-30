from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import User, TargetRole, JobRequirement, UserSkill, Roadmap
from app.schemas.schemas import ChatRequest, ChatResponse
from app.api.deps import get_current_user
from app.ai.skill_gap_engine import calculate_skill_gap
from app.ai.assistant import generate_career_assistant_reply

router = APIRouter(prefix="/assistant", tags=["AI Career Assistant"])

@router.post("/chat", response_model=ChatResponse)
def chat_with_career_assistant(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not payload.messages:
        raise HTTPException(status_code=400, detail="No chat messages provided.")
        
    user_msg = payload.messages[-1].content
    
    # Extract Context
    target_role_id = current_user.target_role_id or 1
    role = db.query(TargetRole).filter(TargetRole.id == target_role_id).first()
    role_title = role.title if role else "Software Engineer"
    
    job_reqs = db.query(JobRequirement).filter(JobRequirement.target_role_id == target_role_id).all()
    formatted_job_reqs = [{"skill_id": jr.skill_id, "name": jr.skill.name, "category": jr.skill.category, "required_level": jr.required_level, "importance": jr.importance} for jr in job_reqs]
    
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == current_user.id).all()
    formatted_user_skills = [{"skill_id": us.skill_id, "name": us.skill.name, "proficiency_level": us.proficiency_level} for us in user_skills]
    
    gap_result = calculate_skill_gap(formatted_user_skills, formatted_job_reqs, role_title)
    
    roadmap = db.query(Roadmap).filter(Roadmap.user_id == current_user.id).order_by(Roadmap.id.desc()).first()
    active_proj = "Sales Analytics Dashboard"
    if roadmap:
        proj_step = next((s for s in roadmap.steps if s.project_id is not None), None)
        if proj_step and proj_step.project:
            active_proj = proj_step.project.title
            
    completed_skills_names = [us.skill.name for us in user_skills if us.proficiency_level >= 4]

    context = {
        "user_name": current_user.name,
        "target_role": role_title,
        "match_percentage": gap_result["requirement_match_percentage"],
        "top_gaps": gap_result["top_gaps"],
        "completed_skills": completed_skills_names,
        "active_project": active_proj
    }
    
    reply = generate_career_assistant_reply(user_msg, context)
    return {"reply": reply}
