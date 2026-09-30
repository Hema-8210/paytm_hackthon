from typing import List, Dict, Any
from app.ai.llm_client import llm_client

def generate_personalized_roadmap(
    target_role_title: str,
    skill_gaps: List[Dict[str, Any]],
    recommended_projects: List[Dict[str, Any]],
    weekly_hours: int = 10
) -> Dict[str, Any]:
    """
    Generates a 5-phase personalized learning roadmap mapped to actual database skills and projects.
    """
    high_gaps = [g for g in skill_gaps if g.get("priority") == "High" and g.get("gap", 0) > 0]
    med_gaps = [g for g in skill_gaps if g.get("priority") == "Medium" and g.get("gap", 0) > 0]
    other_gaps = [g for g in skill_gaps if g.get("priority") == "Low" and g.get("gap", 0) > 0]
    
    # Fallback to all gaps if priority filtering yields empty
    active_gaps = high_gaps + med_gaps + other_gaps
    if not active_gaps and skill_gaps:
        active_gaps = skill_gaps

    top_project = recommended_projects[0] if recommended_projects else None
    
    steps = []
    order_idx = 1
    
    # Phase 1: Core Fundamentals
    p1_skill = active_gaps[0] if active_gaps else {"name": f"{target_role_title} Core Syntax", "skill_id": None}
    steps.append({
        "phase_number": 1,
        "phase_title": "PHASE 1: Core Fundamentals",
        "title": f"Master {p1_skill['name']} Fundamentals",
        "description": f"Build foundational proficiency in {p1_skill['name']}. Focus on core syntax, primary data models, and basic operational concepts.",
        "order_index": order_idx,
        "skill_id": p1_skill.get("skill_id"),
        "skill_name": p1_skill["name"],
        "project_id": None,
        "project_title": None,
        "status": "not_started"
    })
    order_idx += 1
        
    # Phase 2: Advanced Techniques
    p2_skill = active_gaps[1] if len(active_gaps) > 1 else p1_skill
    steps.append({
        "phase_number": 2,
        "phase_title": "PHASE 2: Advanced Techniques",
        "title": f"Advanced {p2_skill['name']} & Best Practices",
        "description": f"Deepen your expertise in {p2_skill['name']}. Practice complex logic, optimization, and industry standards.",
        "order_index": order_idx,
        "skill_id": p2_skill.get("skill_id"),
        "skill_name": p2_skill["name"],
        "project_id": None,
        "project_title": None,
        "status": "not_started"
    })
    order_idx += 1
        
    # Phase 3: Ecosystem Tools
    p3_skill = active_gaps[2] if len(active_gaps) > 2 else (active_gaps[0] if active_gaps else {"name": "Version Control & Workflow", "skill_id": None})
    steps.append({
        "phase_number": 3,
        "phase_title": "PHASE 3: Ecosystem Tools",
        "title": f"Integrate {p3_skill['name']} into your Stack",
        "description": f"Learn to use {p3_skill['name']} alongside your main tools to build production-grade solutions.",
        "order_index": order_idx,
        "skill_id": p3_skill.get("skill_id"),
        "skill_name": p3_skill["name"],
        "project_id": None,
        "project_title": None,
        "status": "not_started"
    })
    order_idx += 1
        
    # Phase 4: Portfolio Project Application
    proj_title = top_project['title'] if top_project else f"Custom {target_role_title} Portfolio Project"
    proj_desc = f"Apply your learned skills to construct '{proj_title}'. Estimated time: {top_project['estimated_hours'] if top_project else 15} hours. " + (top_project.get('why_recommended', '') if top_project else '')
    steps.append({
        "phase_number": 4,
        "phase_title": "PHASE 4: Practical Portfolio Project",
        "title": f"Build: {proj_title}",
        "description": proj_desc,
        "order_index": order_idx,
        "skill_id": None,
        "skill_name": None,
        "project_id": top_project.get("id") if top_project else None,
        "project_title": proj_title,
        "status": "not_started"
    })
    order_idx += 1
        
    # Phase 5: Job Preparation & Career Launch
    steps.append({
        "phase_number": 5,
        "phase_title": "PHASE 5: Career Launch & Interview Prep",
        "title": f"Tailor Resume & Portfolio for {target_role_title}",
        "description": f"Highlight your newly completed project ({proj_title}) on your resume and practice technical interview questions.",
        "order_index": order_idx,
        "skill_id": None,
        "skill_name": None,
        "project_id": None,
        "project_title": None,
        "status": "not_started"
    })
    
    roadmap_title = f"{target_role_title} Mastery Roadmap"
    summary = f"Customized 5-phase path designed for {weekly_hours} hours/week. Direct target: {p1_skill['name']}."
    
    return {
        "title": roadmap_title,
        "summary": summary,
        "target_role_title": target_role_title,
        "steps": steps
    }
