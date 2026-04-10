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
    input_mode = st.radio(
        "Mode",
        options=["Tailor existing resume", "Build resume from profile + JD"],
        index=0,
    )
    upload_required = input_mode == "Tailor existing resume"
    uploaded_file = st.file_uploader("Upload resume PDF", type=["pdf"], disabled=not upload_required)
    job_url = st.text_input("Job link (optional)")
    job_description = st.text_area("Paste job description", height=220)
    thread_id = st.text_input("Thread ID", value="job-agent-thread-1")

    st.subheader("Profile Details")
    candidate_name = st.text_input("Full name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    location = st.text_input("Location")
    target_role = st.text_input("Target role")
    years_of_experience = st.text_input("Years of experience")
    linkedin_url = st.text_input("LinkedIn URL")
    github_url = st.text_input("GitHub URL")
    portfolio_url = st.text_input("Portfolio URL")
    skills_text = st.text_area("Skills", height=120, placeholder="Python, FastAPI, LangGraph, SQL, Docker")
    experience_text = st.text_area("Experience", height=160, placeholder="Add internships, jobs, responsibilities, and achievements")
    projects_text = st.text_area("Projects", height=140, placeholder="Describe relevant projects with impact and tech stack")
    education_text = st.text_area("Education", height=120, placeholder="Degree, college, graduation year, GPA if useful")
    certifications_text = st.text_area("Certifications", height=100, placeholder="Optional certifications")

    analyze_clicked = st.button("Run analysis", use_container_width=True)

if analyze_clicked:
    if upload_required and not uploaded_file:
        st.error("Please upload a resume PDF.")
    elif not job_url and not job_description.strip():
        st.error("Please provide either a job link or a job description.")
    elif not upload_required and not any([candidate_name, skills_text, experience_text, projects_text, education_text]):
        st.error("Please add some profile information so I can build a resume draft.")
    else:
        saved_resume_path = None
        if uploaded_file is not None:
            saved_resume_path = UPLOAD_DIR / uploaded_file.name
            saved_resume_path.write_bytes(uploaded_file.getbuffer())

        with st.status("Running LangGraph workflow...", expanded=True) as status:
            if upload_required:
                status.write("Planner -> JD Analyzer -> Resume Analyzer -> Gap Detector")
            else:
                status.write("Planner -> JD Analyzer -> Resume Builder -> Gap Detector")
            status.write("Optimizer -> Cover Letter -> Application Answers -> Apply Helper")
            response = analyze_job(
                JobAnalysisRequest(
                    resume_path=str(saved_resume_path) if saved_resume_path else None,
                    job_description=job_description,
                    job_url=job_url,
                    thread_id=thread_id,
                    input_mode="tailor_resume" if upload_required else "build_resume",
                    candidate_name=candidate_name,
                    email=email,
                    phone=phone,
                    location=location,
                    linkedin_url=linkedin_url,
                    github_url=github_url,
                    portfolio_url=portfolio_url,
                    years_of_experience=years_of_experience,
                    target_role=target_role,
                    skills_text=skills_text,
                    education_text=education_text,
                    experience_text=experience_text,
                    projects_text=projects_text,
                    certifications_text=certifications_text,
                )
            )
            st.session_state["analysis_result"] = response
            status.update(label="Analysis complete", state="complete")

result = st.session_state["analysis_result"]

if result:
    left_col, right_col = st.columns([1, 1])
    safe_job_title = (result.job_title or "resume").replace("/", "-").replace("\\", "-").replace(" ", "_")

    with left_col:
        st.subheader("Match Analysis")
        st.metric("Match Score", f"{result.match_score}%")
        st.write("**Mode:**", "Build from profile + JD" if result.input_mode == "build_resume" else "Tailor existing resume")
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
        st.download_button(
            "Download Resume (.txt)",
            data=tailored_resume,
            file_name=f"{safe_job_title}_resume.txt",
            mime="text/plain",
            use_container_width=True,
        )
        cover_letter = st.text_area("Cover Letter", value=result.cover_letter, height=240)
        st.download_button(
            "Download Cover Letter (.txt)",
            data=cover_letter,
            file_name=f"{safe_job_title}_cover_letter.txt",
            mime="text/plain",
            use_container_width=True,
        )

        edited_answers: list[dict[str, str]] = []
        st.write("**Application Answers**")
        for index, item in enumerate(result.application_answers):
            question = item.get("question", f"Question {index + 1}")
            answer = st.text_area(question, value=item.get("answer", ""), height=120, key=f"answer_{index}")
            edited_answers.append({"question": question, "answer": answer})

        answers_text = "\n\n".join(
            f"Q: {item['question']}\nA: {item['answer']}" for item in edited_answers
        )
        st.download_button(
            "Download Application Answers (.txt)",
            data=answers_text,
            file_name=f"{safe_job_title}_application_answers.txt",
            mime="text/plain",
            use_container_width=True,
        )

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
