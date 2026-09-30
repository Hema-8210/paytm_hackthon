from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.models import User, Project, ProjectSkill, TargetRole, JobRequirement, UserSkill
from app.schemas.schemas import ProjectOut
from app.api.deps import get_current_user
from app.ai.skill_gap_engine import calculate_skill_gap
from app.ai.project_recommender import recommend_projects_for_gaps

router = APIRouter(prefix="/projects", tags=["Project Recommendations"])

def format_project_dict(p: Project) -> dict:
    skills_list = []
    for ps in p.project_skills:
        skills_list.append({
            "skill_id": ps.skill_id,
            "skill_name": ps.skill.name,
            "importance": ps.importance
        })
    return {
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "difficulty": p.difficulty,
        "estimated_hours": p.estimated_hours,
        "category": p.category,
        "prerequisites": p.prerequisites,
        "expected_outcome": p.expected_outcome,
        "portfolio_value": p.portfolio_value,
        "implementation_steps": p.implementation_steps or [],
        "skills": skills_list
    }

@router.get("", response_model=List[ProjectOut])
def get_all_projects(
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    skill: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Project)
    if category:
        query = query.filter(Project.category == category)
    if difficulty:
        query = query.filter(Project.difficulty == difficulty)
    if search:
        query = query.filter(Project.title.ilike(f"%{search}%") | Project.description.ilike(f"%{search}%"))
    
    projects = query.all()
    results = [format_project_dict(p) for p in projects]
    
    if skill:
        results = [r for r in results if any(s["skill_name"].lower() == skill.lower() for s in r["skills"])]
        
    return results

@router.get("/recommendations", response_model=List[ProjectOut])
def get_recommended_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Calculate user skill gaps first
    target_role_id = current_user.target_role_id
    if not target_role_id:
        first_role = db.query(TargetRole).first()
        target_role_id = first_role.id if first_role else 1

    role = db.query(TargetRole).filter(TargetRole.id == target_role_id).first()
    job_reqs = db.query(JobRequirement).filter(JobRequirement.target_role_id == target_role_id).all()
    
    formatted_job_reqs = [
        {"skill_id": jr.skill_id, "name": jr.skill.name, "category": jr.skill.category, "required_level": jr.required_level, "importance": jr.importance}
        for jr in job_reqs
    ]
    
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == current_user.id).all()
    formatted_user_skills = [{"skill_id": us.skill_id, "name": us.skill.name, "proficiency_level": us.proficiency_level} for us in user_skills]
    
    gap_result = calculate_skill_gap(formatted_user_skills, formatted_job_reqs, role.title if role else "Target Role")
    
    # Get all projects
    all_projects = [format_project_dict(p) for p in db.query(Project).all()]
    
    recommended = recommend_projects_for_gaps(gap_result["skills"], all_projects)
    return recommended

@router.get("/{project_id}", response_model=ProjectOut)
def get_project_by_id(project_id: int, db: Session = Depends(get_db)):
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return format_project_dict(proj)
