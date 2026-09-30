import re
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Alias dictionary for normalization
SKILL_ALIASES: Dict[str, str] = {
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ts": "TypeScript",
    "typescript": "TypeScript",
    "reactjs": "React",
    "react.js": "React",
    "react": "React",
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "postgres sql": "PostgreSQL",
    "py": "Python",
    "python": "Python",
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",
    "dl": "Deep Learning",
    "deep learning": "Deep Learning",
    "nlp": "Natural Language Processing",
    "natural language processing": "Natural Language Processing",
    "docker": "Docker",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "aws": "AWS",
    "amazon web services": "AWS",
    "gcp": "Google Cloud",
    "google cloud": "Google Cloud",
    "azure": "Microsoft Azure",
    "powerbi": "Power BI",
    "power bi": "Power BI",
    "tableau": "Tableau",
    "excel": "Microsoft Excel",
    "ms excel": "Microsoft Excel",
    "sql": "SQL",
    "nosql": "NoSQL",
    "mongo": "MongoDB",
    "mongodb": "MongoDB",
    "fastapi": "FastAPI",
    "flask": "Flask",
    "django": "Django",
    "express": "Express.js",
    "expressjs": "Express.js",
    "tail wind": "Tailwind CSS",
    "tailwindcss": "Tailwind CSS",
    "html": "HTML5",
    "html5": "HTML5",
    "css": "CSS3",
    "css3": "CSS3",
    "git": "Git",
    "github": "GitHub",
    "cicd": "CI/CD",
    "ci/cd": "CI/CD",
    "rest": "REST APIs",
    "rest api": "REST APIs",
    "restful": "REST APIs",
    "graphql": "GraphQL",
    "devops": "DevOps",
    "scikit": "scikit-learn",
    "scikit-learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "tf": "TensorFlow",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "figma": "Figma",
    "ui/ux": "UI/UX Design",
    "ux": "UI/UX Design",
    "ui": "UI/UX Design",
    "cybersecurity": "Cybersecurity",
    "linux": "Linux",
    "bash": "Bash",
}

def normalize_skill_name(skill_input: str) -> str:
    """Normalizes a raw skill string using alias mapping."""
    clean = skill_input.strip().lower()
    clean_no_punct = re.sub(r'[^\w\s\.\/#\+\-]', '', clean)
    if clean_no_punct in SKILL_ALIASES:
        return SKILL_ALIASES[clean_no_punct]
    if clean in SKILL_ALIASES:
        return SKILL_ALIASES[clean]
    
    # Capitalize appropriately if unknown
    words = skill_input.split()
    return " ".join(w.capitalize() for w in words)

def compute_text_similarity(text1: str, text2: str) -> float:
    """Computes TF-IDF cosine similarity between two text snippets."""
    if not text1 or not text2:
        return 0.0
    try:
        vectorizer = TfidfVectorizer().fit([text1, text2])
        vectors = vectorizer.transform([text1, text2])
        sim = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return float(sim)
    except Exception:
        return 0.0
