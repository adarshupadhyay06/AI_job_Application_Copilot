from __future__ import annotations

import re


COMMON_SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "react",
    "node.js",
    "node",
    "sql",
    "mongodb",
    "postgresql",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "fastapi",
    "django",
    "flask",
    "langgraph",
    "langchain",
    "streamlit",
    "machine learning",
    "deep learning",
    "nlp",
    "pandas",
    "numpy",
    "git",
    "rest api",
    "microservices",
]


def extract_skills(text: str) -> list[str]:
    lowered = text.lower()
    found: list[str] = []
    for skill in COMMON_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, lowered):
            found.append(skill.title())
    return sorted(set(found))


def extract_experience_phrase(text: str) -> str:
    match = re.search(r"(\d+\+?\s*(?:years|yrs).{0,20})", text, flags=re.IGNORECASE)
    return match.group(1).strip() if match else "Not clearly specified"


def short_summary(text: str, limit: int = 500) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned[:limit] + ("..." if len(cleaned) > limit else "")


def extract_company_name(title: str) -> str:
    if " - " in title:
        return title.split(" - ")[-1].strip()
    if "|" in title:
        return title.split("|")[0].strip()
    return "Target Company"
