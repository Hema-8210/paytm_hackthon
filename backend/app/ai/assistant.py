from typing import Dict, Any, List
from app.ai.llm_client import llm_client

def generate_career_assistant_reply(
    user_message: str,
    context: Dict[str, Any]
) -> str:
    """
    Synthesizes current user state (name, target role, match %, top gaps, active roadmap)
    and responds with contextual career advice.
    """
    user_name = context.get("user_name", "Developer")
    target_role = context.get("target_role", "Software Engineer")
    match_pct = context.get("match_percentage", 65.0)
    top_gaps = context.get("top_gaps", [])
    completed_skills = context.get("completed_skills", [])
    active_project = context.get("active_project", "Sales Analytics Dashboard")
    
    gaps_str = ", ".join([f"{g['name']} ({g['priority']} Priority)" for g in top_gaps]) if top_gaps else "None! You are well aligned."
    completed_str = ", ".join(completed_skills) if completed_skills else "None recorded yet."
    
    system_prompt = f"""You are SkillPath AI, an expert career mentor and skill gap coach for {user_name}.
    User Profile Context:
    - Target Role: {target_role}
    - Current Requirement Match Score: {match_pct}%
    - Top High Priority Skill Gaps: {gaps_str}
    - Completed Skills: {completed_str}
    - Recommended Active Project: {active_project}

    Guidelines:
    - Be encouraging, clear, and actionable.
    - Refer directly to the user's target role ({target_role}), requirement match score ({match_pct}%), and specific skill gaps ({gaps_str}).
    - Keep responses concise (2 to 4 paragraphs max) with clear bullet points where helpful.
    """
    
    # Smart local fallback response generator if OpenAI API key is unavailable
    msg_lower = user_message.lower()
    
    fallback_text = f"As a target **{target_role}**, your current Requirement Match is **{match_pct}%**.\n\n"
    
    if "what should i learn next" in msg_lower or "learn next" in msg_lower:
        if top_gaps:
            top = top_gaps[0]
            fallback_text += f"I strongly recommend focusing on **{top['name']}** first. It represents your highest priority gap ({top['priority']} Priority) with a {top['gap']}-level proficiency difference.\n\nAfter mastering {top['name']}, transition directly to building **{active_project}**."
        else:
            fallback_text += "You have covered your primary skill gaps! Start building portfolio projects and optimizing your resume for interview calls."
            
    elif "why is" in msg_lower or "important" in msg_lower:
        fallback_text += f"Skills like **{gaps_str.split(' ')[0]}** are core requirements for a **{target_role}** because production systems rely heavily on robust data handling, clean architecture, and framework mastery.\n\nClosing this gap directly increases your Requirement Match score and makes your portfolio stand out to recruiters."
        
    elif "project" in msg_lower:
        fallback_text += f"You should build **{active_project}**. It specifically targets your missing skills ({gaps_str}) and provides a tangible project you can feature on your resume and GitHub."
        
    elif "resume" in msg_lower:
        fallback_text += f"To improve your resume for **{target_role}** roles:\n1. Highlight verified projects like **{active_project}**.\n2. Quantify achievements (e.g. 'Built REST APIs handling 1k req/sec' or 'Optimized SQL query performance by 40%').\n3. Match your technical skills section directly to job requirement keywords."
        
    else:
        fallback_text += f"Based on your profile, your primary focus should be closing your top skill gaps: **{gaps_str}**.\n\nI recommend following your generated roadmap, completing targeted modules for these gaps, and building **{active_project}** to reach 90%+ job readiness!"

    return llm_client.chat_response(system_prompt, user_message, fallback_text)
