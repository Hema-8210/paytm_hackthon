from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    education = Column(String(100), nullable=True) # e.g. B.Tech / B.S. CS
    college = Column(String(150), nullable=True)
    branch = Column(String(100), nullable=True) # e.g. Computer Science
    graduation_year = Column(Integer, nullable=True)
    experience_level = Column(String(50), nullable=True, default="Beginner") # Beginner, Intermediate, Advanced
    target_role_id = Column(Integer, ForeignKey("target_roles.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user_skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")
    target_role = relationship("TargetRole", back_populates="users")
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    roadmaps = relationship("Roadmap", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
    progress_records = relationship("Progress", back_populates="user", cascade="all, delete-orphan")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=False) # e.g. Languages, Frameworks, Databases, Tools, AI/ML, Cloud
    description = Column(Text, nullable=True)
    aliases = Column(Text, nullable=True) # JSON list or comma-separated aliases

    # Relationships
    user_skills = relationship("UserSkill", back_populates="skill")
    job_requirements = relationship("JobRequirement", back_populates="skill")
    project_skills = relationship("ProjectSkill", back_populates="skill")
    learning_resources = relationship("LearningResource", back_populates="skill")


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    proficiency_level = Column(Integer, nullable=False, default=1) # 1-5
    source = Column(String(50), default="manual") # resume, manual, quiz, project
    confidence = Column(Float, default=1.0) # 0.0 - 1.0 (e.g. 0.96 for resume extraction)

    # Relationships
    user = relationship("User", back_populates="user_skills")
    skill = relationship("Skill", back_populates="user_skills")


class TargetRole(Base):
    __tablename__ = "target_roles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False) # Software Development, Data Science, AI, Security, Cloud

    # Relationships
    users = relationship("User", back_populates="target_role")
    job_requirements = relationship("JobRequirement", back_populates="target_role", cascade="all, delete-orphan")
    roadmaps = relationship("Roadmap", back_populates="target_role")


class JobRequirement(Base):
    __tablename__ = "job_requirements"

    id = Column(Integer, primary_key=True, index=True)
    target_role_id = Column(Integer, ForeignKey("target_roles.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    required_level = Column(Integer, nullable=False, default=3) # 1-5
    importance = Column(Float, nullable=False, default=0.8) # 0.1 - 1.0
    frequency = Column(String(50), default="High") # High, Medium, Low

    # Relationships
    target_role = relationship("TargetRole", back_populates="job_requirements")
    skill = relationship("Skill", back_populates="job_requirements")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    extracted_text = Column(Text, nullable=True)
    parsed_sections = Column(JSON, nullable=True) # Extracted education, skills, experience
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="resumes")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(50), nullable=False) # Beginner, Intermediate, Advanced
    estimated_hours = Column(Integer, nullable=False, default=10)
    category = Column(String(100), nullable=False) # Web Development, Data Science, AI/ML, Cybersecurity, Cloud/DevOps
    prerequisites = Column(Text, nullable=True)
    expected_outcome = Column(Text, nullable=True)
    portfolio_value = Column(Text, nullable=True)
    implementation_steps = Column(JSON, nullable=True) # Step-by-step breakdown list

    # Relationships
    project_skills = relationship("ProjectSkill", back_populates="project", cascade="all, delete-orphan")


class ProjectSkill(Base):
    __tablename__ = "project_skills"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    importance = Column(Float, default=0.8)

    # Relationships
    project = relationship("Project", back_populates="project_skills")
    skill = relationship("Skill", back_populates="project_skills")


class LearningResource(Base):
    __tablename__ = "learning_resources"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(500), nullable=False)
    resource_type = Column(String(50), nullable=False) # Article, Video, Course, Documentation, Interactive
    level = Column(String(50), default="Beginner") # Beginner, Intermediate, Advanced

    # Relationships
    skill = relationship("Skill", back_populates="learning_resources")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    priority = Column(String(50), nullable=False) # High, Medium, Low
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="recommendations")
    skill = relationship("Skill")
    project = relationship("Project")


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_role_id = Column(Integer, ForeignKey("target_roles.id"), nullable=False)
    title = Column(String(150), nullable=False)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="roadmaps")
    target_role = relationship("TargetRole", back_populates="roadmaps")
    steps = relationship("RoadmapStep", back_populates="roadmap", cascade="all, delete-orphan", order_by="RoadmapStep.order_index")


class RoadmapStep(Base):
    __tablename__ = "roadmap_steps"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    phase_number = Column(Integer, default=1)
    phase_title = Column(String(100), default="Foundation")
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, nullable=False, default=0)
    status = Column(String(50), default="not_started") # not_started, in_progress, completed

    # Relationships
    roadmap = relationship("Roadmap", back_populates="steps")
    skill = relationship("Skill")
    project = relationship("Project")


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    progress_percentage = Column(Integer, default=0) # 0-100
    status = Column(String(50), default="not_started") # not_started, learning, completed
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="progress_records")
    skill = relationship("Skill")
