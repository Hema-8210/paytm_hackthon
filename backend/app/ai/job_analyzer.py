import re
from typing import Dict, Any, List
from app.ai.skill_extractor import extract_skills_from_text, KNOWN_SKILL_CATEGORIES

def analyze_job_description_text(job_description: str, job_title: str = "Target Role") -> Dict[str, Any]:
    """
    Processes job description text through text cleaning, NLP extraction, normalization, and importance analysis.
    Returns structured required skill profile.
    """
    if not job_description or len(job_description.strip()) < 10:
        raise ValueError("Job description text is too short to analyze.")
        
    # Clean text
    cleaned_text = re.sub(r'\s+', ' ', job_description).strip()
    
    # Extract skills
    extracted = extract_skills_from_text(cleaned_text)
    
    # Calculate relative importance and frequency
    total_matches = sum(item["frequency"] for item in extracted) if extracted else 1
    
    formatted_requirements = []
    for item in extracted:
        # Importance calculation based on term frequency and presence of key requirement terms (e.g. "must", "required", "proficient")
        term_freq = item["frequency"]
        imp_score = min(0.95, round(0.5 + (term_freq / total_matches) * 2.0, 2))
        
        freq_label = "High" if imp_score >= 0.75 else ("Medium" if imp_score >= 0.55 else "Low")
        required_level = 4 if imp_score >= 0.8 else (3 if imp_score >= 0.6 else 2)
        
        formatted_requirements.append({
            "name": item["name"],
            "category": item["category"],
            "required_level": required_level,
            "importance": imp_score,
            "frequency": freq_label
        })
        
    # Sort by importance descending
    formatted_requirements.sort(key=lambda x: x["importance"], reverse=True)
    
    return {
        "role": job_title,
        "total_skills_detected": len(formatted_requirements),
        "skills": formatted_requirements
    }
