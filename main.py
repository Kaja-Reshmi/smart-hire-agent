from agent import run_job_search_agent
import sqlite3
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from applications import (
    save_application,
    get_applications,
    get_application_summary,
    update_application_status,
    delete_application,
)
from matching import rank_jobs, calculate_job_match
from resume_parser import parse_resume_text
from resume_upload import extract_resume_text


app = FastAPI(
    title="SMART HIRE AI Job Search Agent",
    description="An AI-powered job search and recommendation platform",
    version="0.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_PATH = Path(__file__).parent / "jobs.db"


# -------------------- DATABASE --------------------

def get_db_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# -------------------- HOME AND HEALTH --------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to SMART HIRE!",
        "status": "running",
        "features": [
            "Job search",
            "Skill-based job matching",
            "Resume recommendations",
            "Resume upload",
            "Skill gap analysis",
            "Application tracking",
        ],
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


# -------------------- JOB LISTING --------------------

@app.get("/jobs", tags=["Jobs"])
def get_jobs(limit: int = Query(default=20, ge=1, le=500)):
    connection = get_db_connection()

    try:
        rows = connection.execute(
            "SELECT * FROM jobs ORDER BY id LIMIT ?",
            (limit,),
        ).fetchall()

        return {
            "total_returned": len(rows),
            "jobs": [dict(row) for row in rows],
        }
    finally:
        connection.close()


# -------------------- JOB SEARCH --------------------

@app.get("/jobs/search", tags=["Jobs"])
def search_jobs(
    keyword: str = "",
    location: str = "",
    skill: str = "",
):
    query = "SELECT * FROM jobs WHERE 1=1"
    parameters = []

    if keyword.strip():
        query += """
            AND (
                title LIKE ?
                OR company LIKE ?
                OR description LIKE ?
            )
        """
        value = f"%{keyword.strip()}%"
        parameters.extend([value, value, value])

    if location.strip():
        query += " AND location LIKE ?"
        parameters.append(f"%{location.strip()}%")

    if skill.strip():
        query += " AND required_skills LIKE ?"
        parameters.append(f"%{skill.strip()}%")

    query += " ORDER BY id LIMIT 100"

    connection = get_db_connection()

    try:
        rows = connection.execute(query, parameters).fetchall()

        return {
            "total_found": len(rows),
            "filters": {
                "keyword": keyword,
                "location": location,
                "skill": skill,
            },
            "jobs": [dict(row) for row in rows],
        }
    finally:
        connection.close()


# -------------------- SKILL-BASED JOB MATCHING --------------------

@app.get("/jobs/match", tags=["Jobs"])
def match_jobs(
    skills: str,
    location: str = "",
    limit: int = Query(default=10, ge=1, le=100),
):
    candidate_skills = [
        skill.strip()
        for skill in skills.split(",")
        if skill.strip()
    ]

    query = "SELECT * FROM jobs WHERE 1=1"
    parameters = []

    if location.strip():
        query += " AND location LIKE ?"
        parameters.append(f"%{location.strip()}%")

    connection = get_db_connection()

    try:
        rows = connection.execute(query, parameters).fetchall()
        jobs = [dict(row) for row in rows]

        ranked_jobs = rank_jobs(candidate_skills, jobs)

        return {
            "candidate_skills": candidate_skills,
            "total_jobs_analyzed": len(ranked_jobs),
            "recommendations": ranked_jobs[:limit],
        }
    finally:
        connection.close()


# -------------------- RECOMMEND JOBS FROM RESUME TEXT --------------------

@app.get("/resume/recommend", tags=["Resume"])
def recommend_from_resume(
    resume_text: str,
    location: str = "",
    limit: int = Query(default=10, ge=1, le=100),
):
    parsed_resume = parse_resume_text(resume_text)
    candidate_skills = parsed_resume["skills_found"]

    if not candidate_skills:
        return {
            "message": (
                "No recognized skills found. "
                "Try including technical skills in your resume text."
            ),
            "skills_found": [],
            "recommendations": [],
        }

    query = "SELECT * FROM jobs WHERE 1=1"
    parameters = []

    if location.strip():
        query += " AND location LIKE ?"
        parameters.append(f"%{location.strip()}%")

    connection = get_db_connection()

    try:
        rows = connection.execute(query, parameters).fetchall()
        jobs = [dict(row) for row in rows]

        ranked_jobs = rank_jobs(candidate_skills, jobs)

        return {
            "skills_found": candidate_skills,
            "total_skills_found": parsed_resume["total_skills_found"],
            "total_jobs_analyzed": len(ranked_jobs),
            "recommendations": ranked_jobs[:limit],
        }
    finally:
        connection.close()


# -------------------- UPLOAD RESUME --------------------

@app.post("/resume/upload", tags=["Resume"])
async def upload_resume(
    file: UploadFile = File(...),
    location: str = "",
    limit: int = Query(default=10, ge=1, le=100),
):
    filename = file.filename or ""
    extension = Path(filename).suffix.lower()

    if extension not in {".pdf", ".docx"}:
        raise HTTPException(
            status_code=400,
            detail="Upload a PDF or DOCX resume.",
        )

    file_bytes = await file.read()

    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File size must be 5 MB or less.",
        )

    try:
        resume_text = extract_resume_text(filename, file_bytes)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read the resume. Check that the file is valid.",
        )

    parsed_resume = parse_resume_text(resume_text)
    candidate_skills = parsed_resume["skills_found"]

    if not candidate_skills:
        return {
            "filename": filename,
            "message": "No recognized skills found in this resume.",
            "skills_found": [],
            "recommendations": [],
        }

    query = "SELECT * FROM jobs WHERE 1=1"
    parameters = []

    if location.strip():
        query += " AND location LIKE ?"
        parameters.append(f"%{location.strip()}%")

    connection = get_db_connection()

    try:
        rows = connection.execute(query, parameters).fetchall()
        jobs = [dict(row) for row in rows]

        ranked_jobs = rank_jobs(candidate_skills, jobs)

        return {
            "filename": filename,
            "skills_found": candidate_skills,
            "total_skills_found": parsed_resume["total_skills_found"],
            "total_jobs_analyzed": len(ranked_jobs),
            "recommendations": ranked_jobs[:limit],
        }
    finally:
        connection.close()


# -------------------- SKILL GAP ANALYSIS --------------------

@app.get("/skills/gap", tags=["Skills"])
def analyze_skill_gap(
    skills: str,
    job_id: int,
):
    candidate_skills = [
        skill.strip()
        for skill in skills.split(",")
        if skill.strip()
    ]

    connection = get_db_connection()

    try:
        job = connection.execute(
            "SELECT * FROM jobs WHERE id = ?",
            (job_id,),
        ).fetchone()

        if job is None:
            raise HTTPException(
                status_code=404,
                detail="Job not found.",
            )

        job = dict(job)

        result = calculate_job_match(
            candidate_skills,
            job["required_skills"],
        )

        return {
            "job_title": job["title"],
            "company": job["company"],
            "match_percentage": result["match_percentage"],
            "matched_skills": result["matched_skills"],
            "related_skills": result.get("related_skills", []),
            "missing_skills": result["missing_skills"],
            "suggestion": (
                "Focus on learning the missing skills to improve your match."
                if result["missing_skills"]
                else "You have all the listed required skills!"
            ),
        }
    finally:
        connection.close()


# -------------------- APPLICATION TRACKING --------------------

@app.post("/applications", tags=["Applications"])
def create_application(
    job_id: int,
    status: str = "Saved",
    notes: str = "",
):
    result = save_application(job_id, status, notes)

    if "error" in result:
        raise HTTPException(
            status_code=404,
            detail=result["error"],
        )

    return result


@app.get("/applications", tags=["Applications"])
def list_applications():
    applications = get_applications()

    return {
        "total": len(applications),
        "applications": applications,
    }


@app.get("/applications/summary", tags=["Applications"])
def application_summary():
    return get_application_summary()


@app.patch(
    "/applications/{application_id}/status",
    tags=["Applications"],
)
def change_application_status(
    application_id: int,
    status: str,
):
    result = update_application_status(application_id, status)

    if "error" in result:
        raise HTTPException(
            status_code=404,
            detail=result["error"],
        )

    return result


@app.delete(
    "/applications/{application_id}",
    tags=["Applications"],
)
def remove_application(application_id: int):
    result = delete_application(application_id)

    if "error" in result:
        raise HTTPException(
            status_code=404,
            detail=result["error"],
        )

    return result


@app.get("/agent/recommend")
def agent_recommend_jobs(
    skills: str,
    location: str = "",
    experience_level: str = "",
    limit: int = Query(default=10, ge=1, le=100),
):
    candidate_skills = [
        skill.strip()
        for skill in skills.split(",")
        if skill.strip()
    ]

    if not candidate_skills:
        raise HTTPException(
            status_code=400,
            detail="Please provide at least one skill.",
        )

    connection = get_db_connection()

    try:
        rows = connection.execute(
            "SELECT * FROM jobs ORDER BY id"
        ).fetchall()

        jobs = [dict(row) for row in rows]

        result = run_job_search_agent(
            candidate_skills=candidate_skills,
            jobs=jobs,
            experience_level=experience_level or None,
            preferred_location=location or None,
            top_n=limit,
        )

        return result

    finally:
        connection.close()

