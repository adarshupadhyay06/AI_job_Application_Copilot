from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class JobAgentState(TypedDict, total=False):
    messages: Annotated[list, add_messages]
    thread_id: str
    input_mode: str
    resume_path: str
    resume_text: str
    job_description: str
    job_url: str
    job_title: str
    company_name: str
    candidate_profile: dict
    planner_steps: list[str]
    jd_analysis: dict
    resume_analysis: dict
    gap_analysis: dict
    tailored_resume: str
    cover_letter: str
    application_answers: list[dict[str, str]]
    apply_checklist: list[str]
