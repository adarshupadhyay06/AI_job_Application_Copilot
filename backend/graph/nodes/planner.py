from backend.graph.state import JobAgentState


def planner_node(state: JobAgentState) -> dict:
    uses_builder = state.get("input_mode") == "build_resume"

    return {
        "planner_steps": [
            "Analyze the job description",
            "Generate a base resume draft from profile data" if uses_builder else "Analyze the uploaded resume",
            "Compare job needs with resume evidence",
            "Tailor the resume for ATS alignment",
            "Generate a personalized cover letter",
            "Draft application answers",
            "Prepare human approval package",
        ]
    }
