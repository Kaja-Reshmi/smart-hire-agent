
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "jobs.db"


def initialize_applications_table():
    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'Saved',
                notes TEXT DEFAULT '',
                applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(job_id),
                FOREIGN KEY (job_id) REFERENCES jobs(id)
            )
        """)
        connection.commit()
    finally:
        connection.close()


def save_application(job_id, status="Saved", notes=""):
    allowed_statuses = [
        "Saved", "Applied", "Interview", "Rejected", "Offered"
    ]

    if status not in allowed_statuses:
        raise ValueError("Invalid application status")

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        job = connection.execute(
            "SELECT id FROM jobs WHERE id = ?", (job_id,)
        ).fetchone()

        if not job:
            return {"error": "Job not found"}

        connection.execute("""
            INSERT INTO applications (job_id, status, notes)
            VALUES (?, ?, ?)
            ON CONFLICT(job_id) DO UPDATE SET
                status = excluded.status,
                notes = excluded.notes
        """, (job_id, status, notes))

        connection.commit()
        return {
            "message": "Application saved successfully",
            "job_id": job_id,
            "status": status
        }
    finally:
        connection.close()


def get_applications():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        rows = connection.execute("""
            SELECT
                applications.id AS application_id,
                applications.job_id,
                applications.status,
                applications.notes,
                applications.applied_date,
                jobs.title,
                jobs.company,
                jobs.location
            FROM applications
            JOIN jobs ON applications.job_id = jobs.id
            ORDER BY applications.applied_date DESC
        """).fetchall()

        return [dict(row) for row in rows]
    finally:
        connection.close()


initialize_applications_table()

def get_application_summary():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        statuses = ["Saved", "Applied", "Interview", "Rejected", "Offered"]

        summary = {status: 0 for status in statuses}

        rows = connection.execute("""
            SELECT status, COUNT(*) AS total
            FROM applications
            GROUP BY status
        """).fetchall()

        for row in rows:
            if row["status"] in summary:
                summary[row["status"]] = row["total"]

        return {
            "total_applications": sum(summary.values()),
            "status_summary": summary
        }
    finally:
        connection.close()

def update_application_status(application_id, status):
    allowed_statuses = [
        "Saved", "Applied", "Interview", "Rejected", "Offered"
    ]

    if status not in allowed_statuses:
        return {"error": "Invalid application status"}

    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.execute(
            """
            UPDATE applications
            SET status = ?
            WHERE id = ?
            """,
            (status, application_id)
        )

        connection.commit()

        if cursor.rowcount == 0:
            return {"error": "Application not found"}

        return {
            "message": "Application status updated successfully",
            "application_id": application_id,
            "status": status
        }
    finally:
        connection.close()


def delete_application(application_id):
    """Delete a tracked job application by its ID."""
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.execute(
            "DELETE FROM applications WHERE id = ?",
            (application_id,),
        )

        connection.commit()

        if cursor.rowcount == 0:
            return {"error": "Application not found"}

        return {
            "message": "Application deleted successfully",
            "application_id": application_id,
        }
    finally:
        connection.close()

