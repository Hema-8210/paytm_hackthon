import pytest
from app.ai.skill_extractor import extract_skills_from_text
from app.ai.skill_gap_engine import calculate_skill_gap
from app.ai.project_recommender import recommend_projects_for_gaps
from app.ai.roadmap_generator import generate_personalized_roadmap

def test_skill_extraction():
    text = "Experienced with Python, SQL, ReactJS, Docker and AWS for building web applications."
    skills = extract_skills_from_text(text)
    skill_names = [s["name"] for s in skills]
    
    assert "Python" in skill_names
    assert "SQL" in skill_names
    assert "React" in skill_names
    assert "Docker" in skill_names
    assert "AWS" in skill_names

def test_skill_gap_calculation():
    user_skills = [
        {"name": "Python", "proficiency_level": 4},
        {"name": "SQL", "proficiency_level": 2}
    ]
    job_reqs = [
        {"name": "Python", "category": "Languages", "required_level": 4, "importance": 0.9},
        {"name": "SQL", "category": "Database", "required_level": 4, "importance": 0.95},
        {"name": "Power BI", "category": "Data Science", "required_level": 3, "importance": 0.8}
    ]
    
    result = calculate_skill_gap(user_skills, job_reqs, "Data Analyst")
    
    assert result["target_role"] == "Data Analyst"
    assert result["skills_matched"] == 2
    assert result["skills_missing"] == 1
    assert 0 <= result["requirement_match_percentage"] <= 100
    assert len(result["top_gaps"]) > 0

def test_project_recommendations():
    gaps = [
        {"name": "SQL", "gap": 2, "priority": "High", "importance": 0.95},
        {"name": "Power BI", "gap": 3, "priority": "High", "importance": 0.8}
    ]
    projects = [
        {
            "id": 1,
            "title": "Sales Analytics Dashboard",
            "skills": [{"skill_name": "SQL"}, {"skill_name": "Power BI"}]
        },
        {
            "id": 2,
            "title": "React Chat App",
            "skills": [{"skill_name": "React"}]
        }
    ]
    
    recommended = recommend_projects_for_gaps(gaps, projects)
    assert len(recommended) == 1
    assert recommended[0]["title"] == "Sales Analytics Dashboard"

def test_roadmap_generation():
    role_title = "Data Analyst"
    gaps = [{"name": "SQL", "gap": 2, "priority": "High", "skill_id": 1}]
    recommended_projects = [{
        "id": 1,
        "title": "Sales Analytics Dashboard",
        "estimated_hours": 18,
        "difficulty": "Intermediate",
        "why_recommended": "Addresses SQL gap"
    }]
    
    roadmap = generate_personalized_roadmap(role_title, gaps, recommended_projects, 10)
    
    assert "Data Analyst" in roadmap["title"]
    assert len(roadmap["steps"]) >= 4
    assert any("SQL" in s["title"] for s in roadmap["steps"])
