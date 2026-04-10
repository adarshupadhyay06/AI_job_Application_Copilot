from backend.graph.state import JobAgentState
from backend.services.llm_service import llm_service
from backend.utils.text_utils import extract_skills, short_summary


def _build_profile_text(profile: dict) -> str:
    sections = [
        f"Candidate Name: {profile.get('candidate_name', '')}",
        f"Email: {profile.get('email', '')}",
        f"Phone: {profile.get('phone', '')}",
        f"Location: {profile.get('location', '')}",
        f"LinkedIn: {profile.get('linkedin_url', '')}",
        f"GitHub: {profile.get('github_url', '')}",
        f"Portfolio: {profile.get('portfolio_url', '')}",
        f"Years of Experience: {profile.get('years_of_experience', '')}",
        f"Target Role: {profile.get('target_role', '')}",
        f"Skills: {profile.get('skills_text', '')}",
        f"Education: {profile.get('education_text', '')}",
        f"Experience: {profile.get('experience_text', '')}",
        f"Projects: {profile.get('projects_text', '')}",
        f"Certifications: {profile.get('certifications_text', '')}",
    ]
    return "\n".join(section for section in sections if section.split(":", 1)[1].strip())


def resume_builder_node(state: JobAgentState) -> dict:
    profile = state.get("candidate_profile", {})
    profile_text = _build_profile_text(profile)

    fallback = (
        f"{profile.get('candidate_name', 'Candidate')}\n"
        f"{profile.get('email', '')} | {profile.get('phone', '')} | {profile.get('location', '')}\n"
        f"{profile.get('linkedin_url', '')} | {profile.get('github_url', '')} | {profile.get('portfolio_url', '')}\n\n"
        "PROFESSIONAL SUMMARY\n"
        f"A candidate targeting {state.get('job_title', profile.get('target_role', 'the role'))} with "
        f"{profile.get('years_of_experience', 'relevant')} experience.\n\n"
        "SKILLS\n"
        f"{profile.get('skills_text', '')}\n\n"
        "EXPERIENCE\n"
        f"{profile.get('experience_text', '')}\n\n"
        "PROJECTS\n"
        f"{profile.get('projects_text', '')}\n\n"
        "EDUCATION\n"
        f"{profile.get('education_text', '')}\n\n"
        "CERTIFICATIONS\n"
        f"{profile.get('certifications_text', '')}"
    )

    prompt = f"""
You are an expert resume writer.
Create a clean ATS-friendly resume draft from the candidate profile below and lightly align it to the target job description.

Rules:
- Keep everything truthful to the provided profile.
- Do not invent tools, companies, degrees, metrics, or achievements.
- Write concise strong bullet points.
- Use the job description keywords only when they are supported by the profile.
- Include these sections if data exists: header, professional summary, skills, experience, projects, education, certifications.

Target Job Title: {state.get('job_title', profile.get('target_role', 'Job Opening'))}
Company: {state.get('company_name', 'Target Company')}
JD Summary: {state.get('jd_analysis', {}).get('summary', '')}
JD Skills: {state.get('jd_analysis', {}).get('skills', [])}

Candidate Profile:
{profile_text}
"""
    resume_text = llm_service.invoke_text(prompt, fallback)

    return {
        "resume_text": resume_text,
        "resume_analysis": {
            "summary": short_summary(resume_text),
            "skills": extract_skills(resume_text),
            "experience": profile.get("years_of_experience", "Not clearly specified"),
            "projects": [],
        },
    }
