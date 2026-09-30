from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import User, Skill, UserSkill, TargetRole
from app.schemas.schemas import UserOut, OnboardingRequest
from app.api.deps import get_current_user
from app.ai.embeddings import normalize_skill_name

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserOut)
def read_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/onboarding", response_model=UserOut)
def process_onboarding(
    payload: OnboardingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if payload.education:
        current_user.education = payload.education
    if payload.college:
        current_user.college = payload.college
    if payload.branch:
        current_user.branch = payload.branch
    if payload.graduation_year:
        current_user.graduation_year = payload.graduation_year
    if payload.experience_level:
        current_user.experience_level = payload.experience_level
        
    # Process Target Role
    if payload.target_role_id:
        current_user.target_role_id = payload.target_role_id
    elif payload.target_role_title:
        role = db.query(TargetRole).filter(TargetRole.title == payload.target_role_title).first()
        if not role:
            # Create custom role
            role = TargetRole(
                title=payload.target_role_title.strip(),
                category="Custom",
                description="Custom target role created during onboarding."
            )
            db.add(role)
            db.flush()
        current_user.target_role_id = role.id

    # Process skills list
    if payload.skills:
        # Clear existing skills or merge
        for sk_item in payload.skills:
            normalized_name = normalize_skill_name(sk_item.name)
            skill = db.query(Skill).filter(Skill.name == normalized_name).first()
            if not skill:
                skill = Skill(
                    name=normalized_name,
                    category="General",
                    description=f"Skill added: {normalized_name}"
                )
                db.add(skill)
                db.flush()
                
            # Check if user already has skill
            existing_uskill = db.query(UserSkill).filter(
                UserSkill.user_id == current_user.id,
                UserSkill.skill_id == skill.id
            ).first()
            
            if existing_uskill:
                existing_uskill.proficiency_level = sk_item.proficiency_level
            else:
                new_uskill = UserSkill(
                    user_id=current_user.id,
                    skill_id=skill.id,
                    proficiency_level=sk_item.proficiency_level,
                    source="onboarding",
                    confidence=1.0
                )
                db.add(new_uskill)
                
    db.commit()
    db.refresh(current_user)
    return current_user
