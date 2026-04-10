from backend.graph.state import JobAgentState
from backend.services.llm_service import llm_service
from backend.services.pdf_service import extract_text_from_pdf
from backend.utils.text_utils import extract_experience_phrase, extract_skills, short_summary


def resume_analyzer_node(state: JobAgentState) -> dict:
    resume_text = state.get("resume_text", "")
    if not resume_text:
        resume_path = state.get("resume_path")
        if not resume_path:
            raise ValueError("Resume path is required when no generated resume text is available.")
        resume_text = extract_text_from_pdf(resume_path)

    fallback = {
        "summary": short_summary(resume_text),
        "skills": extract_skills(resume_text),
        "experience": extract_experience_phrase(resume_text),
        "projects": [],
    }

    prompt = f"""
You are a resume analyzer.
Review the following resume text and extract structured details.

Resume:
{resume_text}

Return JSON with:
- summary
- skills (list of strings)
- experience
- projects (list of short strings)
"""
    resume_analysis = llm_service.invoke_json(prompt, fallback)

    return {
        "resume_text": resume_text,
        "resume_analysis": resume_analysis,
    }
