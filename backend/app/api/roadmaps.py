from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import User, Roadmap, RoadmapStep, TargetRole, JobRequirement, UserSkill, Project
from app.schemas.schemas import RoadmapOut, GenerateRoadmapRequest
from app.api.deps import get_current_user
from app.ai.skill_gap_engine import calculate_skill_gap
from app.ai.project_recommender import recommend_projects_for_gaps
from app.ai.roadmap_generator import generate_personalized_roadmap
from app.api.projects import format_project_dict

router = APIRouter(prefix="/roadmaps", tags=["AI Roadmap Generator"])

def format_roadmap_response(r: Roadmap) -> dict:
    steps_out = []
    for s in r.steps:
        steps_out.append({
            "id": s.id,
            "phase_number": s.phase_number,
            "phase_title": s.phase_title,
            "title": s.title,
            "description": s.description,
            "order_index": s.order_index,
            "status": s.status,
            "skill_id": s.skill_id,
            "skill_name": s.skill.name if s.skill else None,
            "project_id": s.project_id,
            "project_title": s.project.title if s.project else None
        })
    return {
        "id": r.id,
        "title": r.title,
        "summary": r.summary,
        "target_role_title": r.target_role.title if r.target_role else "Target Role",
        "created_at": r.created_at,
        "steps": steps_out
    }

@router.get("/current", response_model=RoadmapOut)
def get_current_roadmap(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    roadmap = db.query(Roadmap).filter(Roadmap.user_id == current_user.id).order_by(Roadmap.id.desc()).first()
    if not roadmap:
        # Auto-generate roadmap if none exists yet
        return generate_user_roadmap(GenerateRoadmapRequest(), db, current_user)
    return format_roadmap_response(roadmap)

@router.post("/generate", response_model=RoadmapOut)
def generate_user_roadmap(
    payload: GenerateRoadmapRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    target_role_id = current_user.target_role_id
    if not target_role_id:
        first_role = db.query(TargetRole).first()
        target_role_id = first_role.id if first_role else 1

    role = db.query(TargetRole).filter(TargetRole.id == target_role_id).first()
    role_title = role.title if role else "Software Developer"
    
    # Calculate Gaps
    job_reqs = db.query(JobRequirement).filter(JobRequirement.target_role_id == target_role_id).all()
    formatted_job_reqs = [{"skill_id": jr.skill_id, "name": jr.skill.name, "category": jr.skill.category, "required_level": jr.required_level, "importance": jr.importance} for jr in job_reqs]
    
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == current_user.id).all()
    formatted_user_skills = [{"skill_id": us.skill_id, "name": us.skill.name, "proficiency_level": us.proficiency_level} for us in user_skills]
    
    gap_result = calculate_skill_gap(formatted_user_skills, formatted_job_reqs, role_title)
    
    # Get recommended projects
    all_projects = [format_project_dict(p) for p in db.query(Project).all()]
    rec_projects = recommend_projects_for_gaps(gap_result["skills"], all_projects)
    
    # Generate Roadmap dict
    roadmap_dict = generate_personalized_roadmap(role_title, gap_result["skills"], rec_projects, payload.weekly_hours or 10)
    
    # Save Roadmap to DB
    new_roadmap = Roadmap(
        user_id=current_user.id,
        target_role_id=target_role_id,
        title=roadmap_dict["title"],
        summary=roadmap_dict["summary"]
    )
    db.add(new_roadmap)
    db.flush()
    
    for st in roadmap_dict["steps"]:
        r_step = RoadmapStep(
            roadmap_id=new_roadmap.id,
            skill_id=st.get("skill_id"),
            project_id=st.get("project_id"),
            phase_number=st["phase_number"],
            phase_title=st["phase_title"],
            title=st["title"],
            description=st["description"],
            order_index=st["order_index"],
            status="not_started"
        )
        db.add(r_step)
        
    db.commit()
    db.refresh(new_roadmap)
    return format_roadmap_response(new_roadmap)

@router.put("/steps/{step_id}/status")
def update_step_status(
    step_id: int,
    status: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    step = db.query(RoadmapStep).join(Roadmap).filter(
        RoadmapStep.id == step_id,
        Roadmap.user_id == current_user.id
    ).first()
    
    if not step:
        raise HTTPException(status_code=404, detail="Roadmap step not found")
        
    if status not in ["not_started", "in_progress", "completed"]:
        raise HTTPException(status_code=400, detail="Invalid status value.")
        
    step.status = status
    db.commit()
    return {"message": "Status updated successfully", "step_id": step_id, "status": status}
