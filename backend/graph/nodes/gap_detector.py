from backend.graph.state import JobAgentState


def gap_detector_node(state: JobAgentState) -> dict:
    jd_skills = {skill.strip() for skill in state["jd_analysis"].get("skills", []) if skill.strip()}
    resume_skills = {skill.strip() for skill in state["resume_analysis"].get("skills", []) if skill.strip()}

    matched_skills = sorted(jd_skills & resume_skills)
    missing_skills = sorted(jd_skills - resume_skills)

    score = 0
    if jd_skills:
        score = int((len(matched_skills) / len(jd_skills)) * 100)

    return {
        "gap_analysis": {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "match_score": score,
            "needs_optimization": bool(missing_skills or score < 70),
        }
    }
