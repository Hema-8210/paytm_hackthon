import fitz # PyMuPDF
import re
from typing import Dict, Any, List
from app.ai.skill_extractor import extract_skills_from_text

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts raw text from PDF bytes using PyMuPDF."""
    text = ""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text("text") + "\n"
    except Exception as e:
        raise ValueError(f"Failed to read PDF file: {str(e)}")
    return text

def parse_resume_sections(text: str) -> Dict[str, str]:
    """Splits raw resume text into logical sections."""
    lines = text.splitlines()
    sections = {
        "Summary": "",
        "Education": "",
        "Experience": "",
        "Skills": "",
        "Projects": "",
        "Certifications": ""
    }
    
    current_section = "Summary"
    
    section_keywords = {
        "education": "Education",
        "academic background": "Education",
        "experience": "Experience",
        "employment history": "Experience",
        "work experience": "Experience",
        "skills": "Skills",
        "technical skills": "Skills",
        "core competencies": "Skills",
        "projects": "Projects",
        "academic projects": "Projects",
        "certifications": "Certifications",
        "licenses": "Certifications"
    }
    
    for line in lines:
        clean_line = line.strip().lower()
        matched = False
        for kw, sec_name in section_keywords.items():
            if clean_line == kw or clean_line.startswith(kw + ":") or clean_line.startswith(kw + " -"):
                current_section = sec_name
                matched = True
                break
        if not matched:
            sections[current_section] += line + "\n"
            
    return sections

def analyze_resume_file(file_bytes: bytes, file_name: str) -> Dict[str, Any]:
    """
    Main function to analyze a PDF resume.
    Returns structured data with sections, extracted text, and skills with confidence values.
    """
    raw_text = extract_text_from_pdf(file_bytes)
    if not raw_text.strip():
        raise ValueError("The uploaded PDF file contains no readable text.")
        
    sections = parse_resume_sections(raw_text)
    extracted_skills = extract_skills_from_text(raw_text)
    
    # Map extracted skills into required format with confidence percentages
    formatted_skills = []
    for item in extracted_skills:
        formatted_skills.append({
            "name": item["name"],
            "category": item["category"],
            "confidence": item["confidence"],
            "proficiency_level": 3 if item["confidence"] > 0.85 else 2
        })
        
    return {
        "file_name": file_name,
        "extracted_text_preview": raw_text[:300] + "..." if len(raw_text) > 300 else raw_text,
        "sections": sections,
        "extracted_skills": formatted_skills
    }
