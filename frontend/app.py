from __future__ import annotations

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import streamlit as st

from backend.app import analyze_job, approve_run
from backend.schemas import ApprovalPayload, JobAnalysisRequest


UPLOAD_DIR = BASE_DIR / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(page_title="AI Job Application Copilot", layout="wide")
st.title("AI Job Application Copilot")

if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None

with st.sidebar:
    st.subheader("Input")
    uploaded_file = st.file_uploader("Upload resume PDF", type=["pdf"])
    job_url = st.text_input("Job link (optional)")
    job_description = st.text_area("Paste job description", height=220)
    thread_id = st.text_input("Thread ID", value="job-agent-thread-1")

    analyze_clicked = st.button("Run analysis", use_container_width=True)

if analyze_clicked:
    if not uploaded_file:
        st.error("Please upload a resume PDF.")
    elif not job_url and not job_description.strip():
        st.error("Please provide either a job link or a job description.")
    else:
        saved_resume_path = UPLOAD_DIR / uploaded_file.name
        saved_resume_path.write_bytes(uploaded_file.getbuffer())

        with st.status("Running LangGraph workflow...", expanded=True) as status:
            status.write("Planner -> JD Analyzer -> Resume Analyzer -> Gap Detector")
            status.write("Optimizer -> Cover Letter -> Application Answers -> Apply Helper")
            response = analyze_job(
                JobAnalysisRequest(
                    resume_path=str(saved_resume_path),
                    job_description=job_description,
                    job_url=job_url,
                    thread_id=thread_id,
                )
            )
            st.session_state["analysis_result"] = response
            status.update(label="Analysis complete", state="complete")

result = st.session_state["analysis_result"]

if result:
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.subheader("Match Analysis")
        st.metric("Match Score", f"{result.match_score}%")
        st.write("**Job Title:**", result.job_title)
        st.write("**Company:**", result.company_name)
        st.write("**JD Summary:**", result.jd_summary)
        st.write("**JD Skills:**", ", ".join(result.jd_skills) or "No skills extracted")
        st.write("**Resume Skills:**", ", ".join(result.resume_skills) or "No skills extracted")
        st.write("**Missing Skills:**", ", ".join(result.missing_skills) or "No major gaps found")

        st.subheader("Apply Checklist")
        for item in result.apply_checklist:
            st.write(f"- {item}")

    with right_col:
        st.subheader("Human Approval")
        tailored_resume = st.text_area("Tailored Resume", value=result.tailored_resume, height=320)
        cover_letter = st.text_area("Cover Letter", value=result.cover_letter, height=240)

        edited_answers: list[dict[str, str]] = []
        st.write("**Application Answers**")
        for index, item in enumerate(result.application_answers):
            question = item.get("question", f"Question {index + 1}")
            answer = st.text_area(question, value=item.get("answer", ""), height=120, key=f"answer_{index}")
            edited_answers.append({"question": question, "answer": answer})

        if st.button("Approve final content", use_container_width=True):
            approve_run(
                result.run_id,
                ApprovalPayload(
                    tailored_resume=tailored_resume,
                    cover_letter=cover_letter,
                    application_answers=edited_answers,
                    approved=True,
                ),
            )
            st.success("Approved and saved. You can now use the generated content to apply safely.")
