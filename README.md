# AI Job Application Copilot

This project is a LangGraph-based job application copilot that:

- analyzes a job description
- parses a resume PDF
- finds skill gaps
- tailors the resume
- writes a cover letter
- drafts common application answers
- asks for human approval before applying

The implementation intentionally stays close to the style of the CampusX `chatbot-in-langgraph` repo:

- simple `StateGraph` flow
- simple LangGraph checkpointer
- Streamlit frontend
- small node functions instead of heavy abstractions

## Project structure

```text
resume_maker/
├── backend/
│   ├── app.py
│   ├── db/
│   ├── graph/
│   │   ├── main_graph.py
│   │   ├── nodes/
│   │   └── state.py
│   ├── schemas.py
│   ├── services/
│   └── utils/
├── frontend/
│   └── app.py
└── requirements.txt
```

## LangGraph flow

```text
START
  -> planner
  -> jd_analyzer
  -> resume_analyzer
  -> gap_detector
  -> optimizer
  -> cover_letter
  -> application_answers
  -> apply_helper
  -> END
```

## Setup

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add environment variables in a `.env` file:

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

The app still works without a Groq key, but it will fall back to simple rule-based outputs.

## Run the Streamlit app

```bash
streamlit run frontend/app.py
```

## Run the FastAPI backend

```bash
uvicorn backend.app:app --reload
```

## Notes

- Resume input expects a PDF path in the backend and a PDF upload in Streamlit.
- Job input can be either a pasted description or a URL.
- The project is designed as an assistive copilot, not a fully automatic job applier.
- Application history and approvals are saved in `backend/db/sqlite.db`.
- Graph session state uses LangGraph's in-memory saver, while durable run history is stored in SQLite.
