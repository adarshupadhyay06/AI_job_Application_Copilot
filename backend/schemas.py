from typing import Any

from pydantic import BaseModel, Field


class JobAnalysisRequest(BaseModel):
    resume_path: str = Field(..., description="Absolute or relative path to the resume PDF")
    job_description: str | None = Field(default=None, description="Raw job description text")
    job_url: str | None = Field(default=None, description="Job post URL to scrape")
    thread_id: str = Field(default="job-agent-thread")


class ApprovalPayload(BaseModel):
    tailored_resume: str
    cover_letter: str
    application_answers: list[dict[str, str]]
    approved: bool = True


class JobAnalysisResponse(BaseModel):
    run_id: str
    job_title: str
    company_name: str
    jd_summary: str
    jd_skills: list[str]
    resume_skills: list[str]
    missing_skills: list[str]
    match_score: int
    tailored_resume: str
    cover_letter: str
    application_answers: list[dict[str, str]]
    apply_checklist: list[str]
    approval_needed: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)
