from __future__ import annotations

import json
import os
import sqlite3
import uuid
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sqlite.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS application_runs (
            id TEXT PRIMARY KEY,
            thread_id TEXT NOT NULL,
            company_name TEXT,
            job_title TEXT,
            jd_summary TEXT,
            jd_skills TEXT,
            resume_skills TEXT,
            missing_skills TEXT,
            match_score INTEGER,
            tailored_resume TEXT,
            cover_letter TEXT,
            application_answers TEXT,
            apply_checklist TEXT,
            approved INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    connection.commit()
    connection.close()


def save_application_run(payload: dict[str, Any]) -> str:
    initialize_database()
    run_id = str(uuid.uuid4())
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO application_runs (
            id, thread_id, company_name, job_title, jd_summary, jd_skills,
            resume_skills, missing_skills, match_score, tailored_resume,
            cover_letter, application_answers, apply_checklist, approved
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_id,
            payload["thread_id"],
            payload["company_name"],
            payload["job_title"],
            payload["jd_summary"],
            json.dumps(payload["jd_skills"]),
            json.dumps(payload["resume_skills"]),
            json.dumps(payload["missing_skills"]),
            payload["match_score"],
            payload["tailored_resume"],
            payload["cover_letter"],
            json.dumps(payload["application_answers"]),
            json.dumps(payload["apply_checklist"]),
            0,
        ),
    )
    connection.commit()
    connection.close()
    return run_id


def mark_run_approved(run_id: str, approved_payload: dict[str, Any]) -> None:
    initialize_database()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE application_runs
        SET tailored_resume = ?, cover_letter = ?, application_answers = ?, approved = 1
        WHERE id = ?
        """,
        (
            approved_payload["tailored_resume"],
            approved_payload["cover_letter"],
            json.dumps(approved_payload["application_answers"]),
            run_id,
        ),
    )
    connection.commit()
    connection.close()
