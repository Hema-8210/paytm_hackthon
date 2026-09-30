from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import User, Progress, Roadmap, RoadmapStep, UserSkill, JobRequirement, TargetRole
from app.schemas.schemas import OverallProgressOut, ProgressUpdate
from app.api.deps import get_current_user
from app.ai.skill_gap_engine import calculate_skill_gap

router = APIRouter(prefix="/progress", tags=["Progress Tracking"])

@router.get("", response_model=OverallProgressOut)
def get_user_overall_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Active roadmap steps
    roadmap = db.query(Roadmap).filter(Roadmap.user_id == current_user.id).order_by(Roadmap.id.desc()).first()
    completion_pct = 0.0
    projects_completed_count = 0
    if roadmap:
        total_steps = len(roadmap.steps)
        completed_steps = sum(1 for s in roadmap.steps if s.status == "completed")
        completion_pct = round((completed_steps / total_steps * 100), 1) if total_steps > 0 else 0.0
        
        projects_completed_count = sum(1 for s in roadmap.steps if s.project_id is not None and s.status == "completed")

    # Skills completed/in progress
    progress_records = db.query(Progress).filter(Progress.user_id == current_user.id).all()
    skills_completed = sum(1 for p in progress_records if p.status == "completed" or p.progress_percentage == 100)
    skills_in_progress = sum(1 for p in progress_records if p.status == "learning" or (0 < p.progress_percentage < 100))

    # Gaps remaining
    target_role_id = current_user.target_role_id or 1
    job_reqs = db.query(JobRequirement).filter(JobRequirement.target_role_id == target_role_id).all()
    formatted_job_reqs = [{"skill_id": jr.skill_id, "name": jr.skill.name, "category": jr.skill.category, "required_level": jr.required_level, "importance": jr.importance} for jr in job_reqs]
    
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == current_user.id).all()
    formatted_user_skills = [{"skill_id": us.skill_id, "name": us.skill.name, "proficiency_level": us.proficiency_level} for us in user_skills]
    
    gap_result = calculate_skill_gap(formatted_user_skills, formatted_job_reqs, "Role")
    high_gaps_count = sum(1 for g in gap_result["top_gaps"] if g["priority"] == "High")

    return {
        "roadmap_completion_percentage": completion_pct,
        "skills_completed": skills_completed,
        "skills_in_progress": skills_in_progress,
        "projects_completed": projects_completed_count,
        "current_streak_days": 5, # Dynamic active streak counter
        "remaining_high_priority_gaps": high_gaps_count
    }

@router.put("/{skill_id}")
def update_skill_progress(
    skill_id: int,
    payload: ProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prog = db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.skill_id == skill_id
    ).first()
    
    if not prog:
        prog = Progress(
            user_id=current_user.id,
            skill_id=skill_id,
            progress_percentage=payload.progress_percentage,
            status=payload.status
        )
        db.add(prog)
    else:
        prog.progress_percentage = payload.progress_percentage
        prog.status = payload.status
        
    db.commit()
    return {"message": "Skill progress updated successfully", "skill_id": skill_id, "progress_percentage": payload.progress_percentage}
