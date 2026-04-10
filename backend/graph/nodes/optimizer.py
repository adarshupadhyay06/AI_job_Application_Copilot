from backend.graph.state import JobAgentState
from backend.services.llm_service import llm_service


def optimizer_node(state: JobAgentState) -> dict:
    jd_skills = state["jd_analysis"].get("skills", [])
    missing_skills = state["gap_analysis"].get("missing_skills", [])
    resume_text = state["resume_text"]

    fallback = (
        "TAILORED RESUME SUMMARY\n"
        f"- Target role: {state['job_title']}\n"
        f"- Strong overlap skills: {', '.join(state['gap_analysis'].get('matched_skills', [])) or 'Not identified'}\n"
        f"- Skills to highlight carefully: {', '.join(missing_skills) or 'None'}\n\n"
        "ORIGINAL RESUME CONTENT\n"
        f"{resume_text}"
    )

    prompt = f"""
You are an expert resume optimizer.
Tailor the resume below for the target role.

Rules:
- Keep the content truthful.
- Do not invent achievements or skills.
- Rewrite bullet points to sound stronger and more aligned to the JD.
- Add a short professional summary at the top.
- Mention relevant job keywords naturally.
- If a skill is missing in the resume, do not fake experience with it.

Target Job Title: {state['job_title']}
Target Company: {state['company_name']}
JD Skills: {jd_skills}
Missing Skills: {missing_skills}

Resume:
{resume_text}
"""

    tailored_resume = llm_service.invoke_text(prompt, fallback)
    return {"tailored_resume": tailored_resume}
