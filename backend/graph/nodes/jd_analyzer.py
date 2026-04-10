from backend.graph.state import JobAgentState
from backend.services.llm_service import llm_service
from backend.services.scraper_service import scrape_job_post
from backend.utils.text_utils import extract_company_name, extract_experience_phrase, extract_skills, short_summary


def jd_analyzer_node(state: JobAgentState) -> dict:
    job_description = state.get("job_description") or ""
    job_title = state.get("job_title") or "Job Opening"
    company_name = state.get("company_name") or "Target Company"

    if state.get("job_url") and not job_description.strip():
        scraped = scrape_job_post(state["job_url"])
        job_description = scraped["content"]
        job_title = scraped["title"]
        company_name = extract_company_name(scraped["title"])

    fallback = {
        "summary": short_summary(job_description),
        "skills": extract_skills(job_description),
        "experience": extract_experience_phrase(job_description),
    }

    prompt = f"""
You are a job description analyzer.
Extract the most important information from the following job description.

Job Title: {job_title}
Company: {company_name}

Job Description:
{job_description}

Return JSON with:
- summary
- skills (list of strings)
- experience
"""
    jd_analysis = llm_service.invoke_json(prompt, fallback)

    return {
        "job_description": job_description,
        "job_title": job_title,
        "company_name": company_name,
        "jd_analysis": jd_analysis,
    }
