from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import User, Resume, Skill, UserSkill
from app.schemas.schemas import ResumeAnalysisResponse, ConfirmSkillsRequest, UserOut
from app.api.deps import get_current_user
from app.ai.resume_analyzer import analyze_resume_file
from app.ai.embeddings import normalize_skill_name

router = APIRouter(prefix="/resume", tags=["Resume Analyzer"])

@router.post("/upload", response_model=ResumeAnalysisResponse)
async def upload_and_analyze_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a valid PDF document.")
        
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 10 MB limit.")

    try:
        analysis = analyze_resume_file(contents, file.filename)
        
        # Save resume record
        resume_record = Resume(
            user_id=current_user.id,
            file_name=file.filename,
            extracted_text=analysis["extracted_text_preview"],
            parsed_sections=analysis["sections"]
        )
        db.add(resume_record)
        db.commit()
        db.refresh(resume_record)
        
        # Link skill IDs if available
        for sk in analysis["extracted_skills"]:
            existing_sk = db.query(Skill).filter(Skill.name.ilike(sk["name"])).first()
            if existing_sk:
                sk["skill_id"] = existing_sk.id
                
        return {
            "resume_id": resume_record.id,
            "file_name": file.filename,
            "extracted_text_preview": analysis["extracted_text_preview"],
            "sections": analysis["sections"],
            "extracted_skills": analysis["extracted_skills"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to analyze resume. {str(e)}")

@router.post("/confirm-skills", response_model=UserOut)
def confirm_resume_skills(
    payload: ConfirmSkillsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    for sk_item in payload.skills:
        normalized = normalize_skill_name(sk_item.name)
        skill = db.query(Skill).filter(Skill.name == normalized).first()
        if not skill:
            skill = Skill(name=normalized, category="General", description=f"Skill: {normalized}")
            db.add(skill)
            db.flush()
            
        existing_uskill = db.query(UserSkill).filter(
            UserSkill.user_id == current_user.id,
            UserSkill.skill_id == skill.id
        ).first()
        
        if existing_uskill:
            existing_uskill.proficiency_level = max(existing_uskill.proficiency_level, sk_item.proficiency_level)
            existing_uskill.source = "resume"
        else:
            new_uskill = UserSkill(
                user_id=current_user.id,
                skill_id=skill.id,
                proficiency_level=sk_item.proficiency_level,
                source="resume",
                confidence=0.92
            )
            db.add(new_uskill)

    db.commit()
    db.refresh(current_user)
    return current_user
