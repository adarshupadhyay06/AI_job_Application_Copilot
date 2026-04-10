from fastapi import FastAPI, HTTPException

from backend.db.persistence import mark_run_approved, save_application_run
from backend.graph.main_graph import job_agent
from backend.schemas import ApprovalPayload, JobAnalysisRequest, JobAnalysisResponse


app = FastAPI(title="AI Job Application Copilot")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze", response_model=JobAnalysisResponse)
def analyze_job(request: JobAnalysisRequest) -> JobAnalysisResponse:
    candidate_profile = {
        "candidate_name": request.candidate_name or "",
        "email": request.email or "",
        "phone": request.phone or "",
        "location": request.location or "",
        "linkedin_url": request.linkedin_url or "",
        "github_url": request.github_url or "",
        "portfolio_url": request.portfolio_url or "",
        "years_of_experience": request.years_of_experience or "",
        "target_role": request.target_role or "",
        "skills_text": request.skills_text or "",
        "education_text": request.education_text or "",
        "experience_text": request.experience_text or "",
        "projects_text": request.projects_text or "",
        "certifications_text": request.certifications_text or "",
    }

    result = job_agent.invoke(
        {
            "thread_id": request.thread_id,
            "input_mode": request.input_mode,
            "resume_path": request.resume_path or "",
            "job_description": request.job_description or "",
            "job_url": request.job_url or "",
            "job_title": "Job Opening",
            "company_name": "Target Company",
            "candidate_profile": candidate_profile,
        },
        config={"configurable": {"thread_id": request.thread_id}},
    )

    payload = {
        "thread_id": request.thread_id,
        "company_name": result["company_name"],
        "job_title": result["job_title"],
        "jd_summary": result["jd_analysis"].get("summary", ""),
        "jd_skills": result["jd_analysis"].get("skills", []),
        "resume_skills": result["resume_analysis"].get("skills", []),
        "missing_skills": result["gap_analysis"].get("missing_skills", []),
        "match_score": result["gap_analysis"].get("match_score", 0),
        "tailored_resume": result["tailored_resume"],
        "cover_letter": result["cover_letter"],
        "application_answers": result["application_answers"],
        "apply_checklist": result["apply_checklist"],
    }
    run_id = save_application_run(payload)

    return JobAnalysisResponse(
        run_id=run_id,
        input_mode=request.input_mode,
        **payload,
        approval_needed=True,
        metadata={"planner_steps": result.get("planner_steps", [])},
    )


@app.post("/approve/{run_id}")
def approve_run(run_id: str, approval: ApprovalPayload) -> dict[str, str]:
    if not approval.approved:
        raise HTTPException(status_code=400, detail="Approval payload marked as not approved.")

    mark_run_approved(run_id, approval.model_dump())
    return {"status": "approved", "run_id": run_id}
