from typing import List, Dict, Any

def calculate_skill_gap(
    current_user_skills: List[Dict[str, Any]],
    job_requirements: List[Dict[str, Any]],
    target_role_title: str = "Target Role"
) -> Dict[str, Any]:
    """
    Computes deterministic skill gaps, priority scores, requirement match %, and top gaps.
    
    current_user_skills: [{"skill_id": int, "name": str, "proficiency_level": int (1-5)}]
    job_requirements: [{"skill_id": int, "name": str, "category": str, "required_level": int (1-5), "importance": float}]
    """
    # Create lookup map for user skills
    user_skill_map = {
        s["name"].lower(): s.get("proficiency_level", 1)
        for s in current_user_skills
    }
    
    gap_items = []
    total_importance = 0.0
    attained_weighted_score = 0.0
    matched_count = 0
    missing_count = 0
    
    for req in job_requirements:
        req_name = req["name"]
        req_name_lower = req_name.lower()
        req_level = req.get("required_level", 3)
        importance = req.get("importance", 0.8)
        category = req.get("category", "General")
        skill_id = req.get("skill_id", 0)
        
        current_level = user_skill_map.get(req_name_lower, 0)
        if current_level > 0:
            matched_count += 1
        else:
            missing_count += 1
            
        gap = max(0, req_level - current_level)
        priority_score = round(gap * importance, 2)
        
        if priority_score >= 1.5 or (gap >= 2 and importance >= 0.7):
            priority = "High"
        elif priority_score >= 0.8 or gap >= 1:
            priority = "Medium"
        else:
            priority = "Low"
            
        gap_items.append({
            "skill_id": skill_id,
            "name": req_name,
            "category": category,
            "current_level": current_level,
            "required_level": req_level,
            "gap": gap,
            "importance": importance,
            "priority": priority,
            "priority_score": priority_score
        })
        
        total_importance += importance
        attained_ratio = min(1.0, current_level / req_level) if req_level > 0 else 1.0
        attained_weighted_score += (attained_ratio * importance)
        
    # Sort gap items by priority_score descending
    gap_items.sort(key=lambda x: (x["priority_score"], x["importance"]), reverse=True)
    
    # Requirement Match Score (0 - 100%)
    match_percentage = round((attained_weighted_score / total_importance * 100), 1) if total_importance > 0 else 100.0
    match_percentage = max(0.0, min(100.0, match_percentage))
    
    # Extract top gaps
    top_gaps = [item for item in gap_items if item["gap"] > 0][:4]
    
    # Generate single Recommended Next Step
    recommended_next_step = "Your skill profile is fully aligned with this role! Consider preparing your portfolio."
    if top_gaps:
        top_skill = top_gaps[0]
        recommended_next_step = f"Focus on mastering {top_skill['name']} ({top_skill['priority']} Priority Gap of {top_skill['gap']} levels) through practical project building."
        
    return {
        "target_role": target_role_title,
        "requirement_match_percentage": match_percentage,
        "total_required_skills": len(job_requirements),
        "skills_matched": matched_count,
        "skills_missing": missing_count,
        "skills": gap_items,
        "top_gaps": top_gaps,
        "recommended_next_step": recommended_next_step
    }
