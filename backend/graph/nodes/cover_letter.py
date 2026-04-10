from backend.graph.state import JobAgentState
from backend.services.llm_service import llm_service


def cover_letter_node(state: JobAgentState) -> dict:
    fallback = (
        f"Dear Hiring Team,\n\n"
        f"I am excited to apply for the {state['job_title']} role at {state['company_name']}. "
        f"My background aligns with key requirements such as "
        f"{', '.join(state['gap_analysis'].get('matched_skills', [])[:5]) or 'software development and problem-solving'}. "
        "I enjoy building practical solutions, learning quickly, and collaborating with teams to ship useful products.\n\n"
        "Thank you for your time and consideration.\n"
    )

    prompt = f"""
Write a concise personalized cover letter.

Job Title: {state['job_title']}
Company: {state['company_name']}
JD Summary: {state['jd_analysis'].get('summary', '')}
Matched Skills: {state['gap_analysis'].get('matched_skills', [])}
Resume Summary: {state['resume_analysis'].get('summary', '')}

Keep it under 300 words and professional.
"""
    cover_letter = llm_service.invoke_text(prompt, fallback)
    return {"cover_letter": cover_letter}
