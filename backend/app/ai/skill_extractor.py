import re
from typing import List, Dict, Any
from app.ai.embeddings import normalize_skill_name, SKILL_ALIASES

KNOWN_SKILL_CATEGORIES: Dict[str, str] = {
    "Python": "Languages",
    "Java": "Languages",
    "C": "Languages",
    "C++": "Languages",
    "JavaScript": "Languages",
    "TypeScript": "Languages",
    "Go": "Languages",
    "Rust": "Languages",
    "Ruby": "Languages",
    "PHP": "Languages",
    "SQL": "Database",
    "PostgreSQL": "Database",
    "MySQL": "Database",
    "MongoDB": "Database",
    "Redis": "Database",
    "NoSQL": "Database",
    "React": "Frontend",
    "Vue.js": "Frontend",
    "Angular": "Frontend",
    "Next.js": "Frontend",
    "Tailwind CSS": "Frontend",
    "HTML5": "Frontend",
    "CSS3": "Frontend",
    "Node.js": "Backend",
    "Express.js": "Backend",
    "FastAPI": "Backend",
    "Django": "Backend",
    "Flask": "Backend",
    "Spring Boot": "Backend",
    "REST APIs": "Backend",
    "GraphQL": "Backend",
    "Machine Learning": "AI/ML",
    "Artificial Intelligence": "AI/ML",
    "Deep Learning": "AI/ML",
    "Natural Language Processing": "AI/ML",
    "scikit-learn": "AI/ML",
    "TensorFlow": "AI/ML",
    "PyTorch": "AI/ML",
    "Pandas": "AI/ML",
    "NumPy": "AI/ML",
    "Data Analysis": "Data Science",
    "Power BI": "Data Science",
    "Tableau": "Data Science",
    "Microsoft Excel": "Data Science",
    "Statistics": "Data Science",
    "Docker": "Cloud/DevOps",
    "Kubernetes": "Cloud/DevOps",
    "AWS": "Cloud/DevOps",
    "Google Cloud": "Cloud/DevOps",
    "Microsoft Azure": "Cloud/DevOps",
    "CI/CD": "Cloud/DevOps",
    "Git": "Tools",
    "GitHub": "Tools",
    "Linux": "Tools",
    "Bash": "Tools",
    "Cybersecurity": "Security",
    "UI/UX Design": "Design",
    "Figma": "Design",
}

def extract_skills_from_text(text: str) -> List[Dict[str, Any]]:
    """
    Extracts skills and confidence scores from arbitrary text (resume or JD).
    Returns a list of dicts: [{"name": skill_name, "category": category, "confidence": score, "frequency": count}]
    """
    if not text:
        return []
    
    clean_text = text.lower()
    found_skills: Dict[str, int] = {}
    
    # 1. Check known aliases and canonical terms
    for alias_key, canonical_name in SKILL_ALIASES.items():
        # Match as whole word / bounded term
        pattern = r'\b' + re.escape(alias_key) + r'\b'
        matches = len(re.findall(pattern, clean_text))
        if matches > 0:
            found_skills[canonical_name] = found_skills.get(canonical_name, 0) + matches

    # 2. Check directly against known skill categories
    for skill_name in KNOWN_SKILL_CATEGORIES.keys():
        if skill_name not in found_skills:
            pattern = r'\b' + re.escape(skill_name.lower()) + r'\b'
            matches = len(re.findall(pattern, clean_text))
            if matches > 0:
                found_skills[skill_name] = matches

    # 3. Format results with confidence scores
    results = []
    max_freq = max(found_skills.values()) if found_skills else 1
    
    for skill_name, count in found_skills.items():
        category = KNOWN_SKILL_CATEGORIES.get(skill_name, "General")
        # Confidence calculation: 0.70 + (normalized frequency * 0.28)
        norm_freq = count / max_freq
        confidence = round(min(0.98, 0.72 + (norm_freq * 0.26)), 2)
        
        results.append({
            "name": skill_name,
            "category": category,
            "confidence": confidence,
            "frequency": count
        })
        
    # Sort by confidence descending
    results.sort(key=lambda x: x["confidence"], reverse=True)
    return results
