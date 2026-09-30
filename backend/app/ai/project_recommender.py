from typing import List, Dict, Any

def recommend_projects_for_gaps(
    skill_gaps: List[Dict[str, Any]],
    available_projects: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Ranks available database projects based on user skill gaps.
    
    skill_gaps: output list from skill_gap_engine ("name", "gap", "priority", "importance")
    available_projects: list of projects from DB with project_skills
    """
    gap_skill_names = {item["name"].lower(): item for item in skill_gaps if item["gap"] > 0}
    high_priority_gaps = {name: item for name, item in gap_skill_names.items() if item["priority"] == "High"}
    
    scored_projects = []
    
    for proj in available_projects:
        project_skill_names = [ps["skill_name"].lower() for ps in proj.get("skills", [])]
        
        # Calculate overlap
        addressed_all_gaps = [name for name in project_skill_names if name in gap_skill_names]
        addressed_high_gaps = [name for name in project_skill_names if name in high_priority_gaps]
        
        count_addressed = len(addressed_all_gaps)
        count_high = len(addressed_high_gaps)
        
        if count_addressed == 0:
            # Skip projects that don't address any gaps
            continue
            
        score = (count_high * 3.0) + (count_addressed * 1.5)
        
        if count_high > 0:
            reason = f"Addresses {count_high} of your current high-priority skill gaps ({', '.join(g.title() for g in addressed_high_gaps[:2])})."
        else:
            reason = f"Helps close {count_addressed} skill gap(s) needed for your target role."
            
        proj_copy = dict(proj)
        proj_copy["why_recommended"] = reason
        proj_copy["addressed_gaps_count"] = count_addressed
        proj_copy["recommendation_score"] = score
        
        scored_projects.append(proj_copy)
        
    # Sort by recommendation score descending
    scored_projects.sort(key=lambda x: (x["recommendation_score"], x["addressed_gaps_count"]), reverse=True)
    return scored_projects
