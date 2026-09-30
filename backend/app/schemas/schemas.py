from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any
from datetime import datetime

# --- Auth Schemas ---
class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None

# --- User Profile & Onboarding ---
class SkillAddManual(BaseModel):
    skill_id: Optional[int] = None
    name: str
    proficiency_level: int = Field(1, ge=1, le=5)

class OnboardingRequest(BaseModel):
    education: Optional[str] = None
    college: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    experience_level: Optional[str] = "Beginner"
    target_role_id: Optional[int] = None
    target_role_title: Optional[str] = None
    skills: List[SkillAddManual] = []

class TargetRoleOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    category: str

    class Config:
        from_attributes = True

class UserSkillOut(BaseModel):
    id: int
    skill_id: int
    skill_name: str
    category: str
    proficiency_level: int
    source: str
    confidence: float

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    education: Optional[str]
    college: Optional[str]
    branch: Optional[str]
    graduation_year: Optional[int]
    experience_level: Optional[str]
    target_role_id: Optional[int]
    target_role: Optional[TargetRoleOut] = None
    skills: List[UserSkillOut] = []
    created_at: datetime

    class Config:
        from_attributes = True

# --- Skill Schemas ---
class SkillOut(BaseModel):
    id: int
    name: str
    category: str
    description: Optional[str]

    class Config:
        from_attributes = True

# --- Resume Analysis Schemas ---
class ExtractedSkill(BaseModel):
    skill_id: Optional[int] = None
    name: str
    category: str = "General"
    confidence: float # 0.0 to 1.0 (e.g., 0.96)
    proficiency_level: int = 3

class ResumeAnalysisResponse(BaseModel):
    resume_id: int
    file_name: str
    extracted_text_preview: str
    sections: dict
    extracted_skills: List[ExtractedSkill]

class ConfirmSkillsRequest(BaseModel):
    skills: List[SkillAddManual]

# --- Job Description Analysis Schemas ---
class JobAnalysisRequest(BaseModel):
    target_role_id: Optional[int] = None
    job_title: Optional[str] = None
    job_description: str

class RequiredSkillItem(BaseModel):
    skill_id: Optional[int] = None
    name: str
    category: str
    required_level: int # 1-5
    importance: float # 0.0 - 1.0
    frequency: str # High, Medium, Low

class JobAnalysisResponse(BaseModel):
    role: str
    total_skills_detected: int
    skills: List[RequiredSkillItem]

# --- Skill Gap Schemas ---
class SkillGapItem(BaseModel):
    skill_id: int
    name: str
    category: str
    current_level: int
    required_level: int
    gap: int
    importance: float
    priority: str # High, Medium, Low
    priority_score: float # gap * importance normalized

class SkillGapResponse(BaseModel):
    target_role: str
    requirement_match_percentage: float # e.g. 68%
    total_required_skills: int
    skills_matched: int
    skills_missing: int
    skills: List[SkillGapItem]
    top_gaps: List[SkillGapItem]
    recommended_next_step: str

# --- Project Schemas ---
class ProjectSkillOut(BaseModel):
    skill_id: int
    skill_name: str
    importance: float

class ProjectOut(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    estimated_hours: int
    category: str
    prerequisites: Optional[str]
    expected_outcome: Optional[str]
    portfolio_value: Optional[str]
    implementation_steps: Optional[List[str]] = []
    skills: List[ProjectSkillOut] = []
    why_recommended: Optional[str] = None
    addressed_gaps_count: Optional[int] = 0

    class Config:
        from_attributes = True

# --- Roadmap Schemas ---
class GenerateRoadmapRequest(BaseModel):
    weekly_hours: Optional[int] = 10

class RoadmapStepOut(BaseModel):
    id: int
    phase_number: int
    phase_title: str
    title: str
    description: Optional[str]
    order_index: int
    status: str
    skill_id: Optional[int]
    skill_name: Optional[str]
    project_id: Optional[int]
    project_title: Optional[str]

    class Config:
        from_attributes = True

class RoadmapOut(BaseModel):
    id: int
    title: str
    summary: Optional[str]
    target_role_title: str
    created_at: datetime
    steps: List[RoadmapStepOut] = []

    class Config:
        from_attributes = True

# --- Learning Resource & Progress Schemas ---
class LearningResourceOut(BaseModel):
    id: int
    skill_id: int
    title: str
    description: Optional[str]
    url: str
    resource_type: str
    level: str

class ProgressUpdate(BaseModel):
    progress_percentage: int = Field(..., ge=0, le=100)
    status: str # not_started, learning, completed

class OverallProgressOut(BaseModel):
    roadmap_completion_percentage: float
    skills_completed: int
    skills_in_progress: int
    projects_completed: int
    current_streak_days: int
    remaining_high_priority_gaps: int

# --- AI Assistant Chat Schemas ---
class ChatMessage(BaseModel):
    role: str # user or assistant
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    reply: str
