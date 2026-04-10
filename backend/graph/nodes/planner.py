from backend.graph.state import JobAgentState


def planner_node(state: JobAgentState) -> dict:
    return {
        "planner_steps": [
            "Analyze the job description",
            "Analyze the uploaded resume",
            "Compare job needs with resume evidence",
            "Tailor the resume for ATS alignment",
            "Generate a personalized cover letter",
            "Draft application answers",
            "Prepare human approval package",
        ]
    }
