from backend.graph.state import JobAgentState


def apply_helper_node(state: JobAgentState) -> dict:
    missing_skills = state["gap_analysis"].get("missing_skills", [])
    checklist = [
        "Review the tailored resume and make any final edits.",
        "Review the cover letter and customize the greeting if you know the hiring manager.",
        "Copy the generated application answers into the form and adjust tone if needed.",
        "Open the job page and autofill only after verifying each field.",
    ]

    if missing_skills:
        checklist.append(
            "Be prepared to explain how your current experience can transfer to these missing skills: "
            + ", ".join(missing_skills)
        )

    return {"apply_checklist": checklist}
