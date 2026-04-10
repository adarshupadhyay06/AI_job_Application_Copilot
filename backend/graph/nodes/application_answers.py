from backend.graph.state import JobAgentState
from backend.services.llm_service import llm_service


def application_answers_node(state: JobAgentState) -> dict:
    fallback = [
        {
            "question": "Why should we hire you?",
            "answer": (
                f"My experience aligns with the {state['job_title']} role, especially in "
                f"{', '.join(state['gap_analysis'].get('matched_skills', [])[:4]) or 'building reliable software'}. "
                "I can contribute quickly while continuing to learn the stack deeply."
            ),
        },
        {
            "question": "Why do you want to work here?",
            "answer": (
                f"I’m interested in {state['company_name']} because the role matches my strengths "
                "and gives me the chance to solve meaningful product and engineering problems."
            ),
        },
        {
            "question": "Describe a relevant project.",
            "answer": state["resume_analysis"].get("summary", "I have worked on projects that improved my end-to-end software development skills."),
        },
    ]

    prompt = f"""
Create short job application answers in JSON array format.
Each item must contain:
- question
- answer

Create answers for:
1. Why should we hire you?
2. Why do you want to work here?
3. Describe a relevant project.

Job Title: {state['job_title']}
Company: {state['company_name']}
JD Summary: {state['jd_analysis'].get('summary', '')}
Resume Summary: {state['resume_analysis'].get('summary', '')}
Matched Skills: {state['gap_analysis'].get('matched_skills', [])}
"""
    application_answers = llm_service.invoke_json(prompt, fallback)

    if not isinstance(application_answers, list):
        application_answers = fallback

    return {"application_answers": application_answers}
