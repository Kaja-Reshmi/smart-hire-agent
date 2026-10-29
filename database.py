
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).parent / "jobs.db"
TARGET_JOB_COUNT = 500
RANDOM_SEED = 42

# Role, department, and skill combinations
ROLE_TEMPLATES = [
    {
        "title": "Machine Learning Engineer",
        "department": "AI/ML",
        "skills": ["Python", "Machine Learning", "Scikit-learn", "Pandas",
                   "NumPy", "SQL", "Model Evaluation"],
    },
    {
        "title": "Data Scientist",
        "department": "Data Science",
        "skills": ["Python", "Statistics", "Pandas", "NumPy",
                   "Machine Learning", "SQL", "Data Visualization"],
    },
    {
        "title": "Data Analyst",
        "department": "Analytics",
        "skills": ["SQL", "Excel", "Python", "Power BI",
                   "Statistics", "Data Visualization"],
    },
    {
        "title": "Python Developer",
        "department": "Software",
        "skills": ["Python", "FastAPI", "Flask", "SQL",
                   "Git", "REST APIs", "Testing"],
    },
    {
        "title": "Java Developer",
        "department": "Software",
        "skills": ["Java", "OOP", "SQL", "Spring Boot",
                   "REST APIs", "Git", "Data Structures"],
    },
    {
        "title": "Full Stack Developer",
        "department": "Web Development",
        "skills": ["JavaScript", "React", "HTML", "CSS",
                   "Node.js", "SQL", "REST APIs"],
    },
    {
        "title": "Frontend Developer",
        "department": "Web Development",
        "skills": ["HTML", "CSS", "JavaScript", "React",
                   "TypeScript", "Responsive Design", "Git"],
    },
    {
        "title": "Backend Developer",
        "department": "Software",
        "skills": ["Python", "SQL", "REST APIs", "Docker",
                   "Authentication", "Git", "Testing"],
    },
    {
        "title": "Cloud Engineer",
        "department": "Cloud",
        "skills": ["AWS", "Linux", "Docker", "Networking",
                   "Python", "CI/CD", "Monitoring"],
    },
    {
        "title": "DevOps Engineer",
        "department": "DevOps",
        "skills": ["Linux", "Docker", "Kubernetes", "CI/CD",
                   "Git", "Cloud Computing", "Monitoring"],
    },
    {
        "title": "Cybersecurity Analyst",
        "department": "Security",
        "skills": ["Networking", "Linux", "Python", "Security Analysis",
                   "Incident Response", "SIEM", "Risk Assessment"],
    },
    {
        "title": "NLP Engineer",
        "department": "AI/ML",
        "skills": ["Python", "NLP", "Transformers", "BERT",
                   "Text Processing", "Machine Learning", "PyTorch"],
    },
    {
        "title": "Computer Vision Engineer",
        "department": "AI/ML",
        "skills": ["Python", "OpenCV", "Deep Learning", "CNN",
                   "NumPy", "PyTorch", "Image Processing"],
    },
    {
        "title": "QA Automation Engineer",
        "department": "Quality Assurance",
        "skills": ["Python", "Selenium", "Pytest", "API Testing",
                   "SQL", "Git", "Test Automation"],
    },
    {
        "title": "Business Analyst",
        "department": "Business",
        "skills": ["SQL", "Excel", "Requirements Analysis",
                   "Communication", "Power BI", "Documentation"],
    },
    {
        "title": "Product Analyst",
        "department": "Product",
        "skills": ["SQL", "Python", "Statistics", "A/B Testing",
                   "Data Visualization", "Product Metrics"],
    },
    {
        "title": "Database Engineer",
        "department": "Data Engineering",
        "skills": ["SQL", "PostgreSQL", "MySQL", "Database Design",
                   "Python", "Query Optimization", "Data Modeling"],
    },
    {
        "title": "Data Engineer",
        "department": "Data Engineering",
        "skills": ["Python", "SQL", "ETL", "Apache Spark",
                   "Data Pipelines", "Airflow", "Cloud Computing"],
    },
    {
        "title": "Mobile App Developer",
        "department": "Mobile Development",
        "skills": ["Java", "Kotlin", "REST APIs", "Git",
                   "UI Design", "Testing", "Mobile Development"],
    },
    {
        "title": "Research Assistant - AI",
        "department": "Research",
        "skills": ["Python", "Machine Learning", "Statistics",
                   "Research", "Data Analysis", "PyTorch"],
    },
]

COMPANIES = [
    "TechNova", "CodeSphere", "DataBridge", "FutureAI",
    "VisionWorks", "CloudPeak", "NexGen Systems", "BrightByte",
    "InnoTech", "Quantum Labs", "BlueOrbit", "PixelCraft",
    "NextWave Technologies", "CoreStack", "Apex Digital",
    "NovaWorks", "Vertex Solutions", "DigitalSpring",
    "Pioneer Analytics", "Skyline Tech",
]

LOCATIONS = [
    "Bengaluru", "Hyderabad", "Chennai", "Pune", "Mumbai",
    "Delhi", "Noida", "Gurugram", "Kochi", "Coimbatore",
    "Kolkata", "Ahmedabad", "Remote",
]

EXPERIENCE_LEVELS = [
    "Internship", "Fresher", "0-1 years", "1-2 years",
    "2-4 years", "4-6 years", "6+ years",
]

WORK_MODES = ["On-site", "Hybrid", "Remote"]

DESCRIPTIONS = [
    "Build, test, and maintain solutions for business requirements.",
    "Collaborate with cross-functional teams to deliver reliable products.",
    "Analyze data, improve workflows, and document technical findings.",
    "Develop scalable applications and troubleshoot technical issues.",
    "Evaluate solutions, measure performance, and improve quality.",
    "Design and implement features while following engineering best practices.",
    "Support product development through experimentation and analysis.",
    "Create maintainable systems and contribute to code reviews.",
]


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT NOT NULL,
                required_skills TEXT NOT NULL,
                experience_level TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)

        # Add optional fields to an existing database safely.
        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(jobs)")
        }

        if "work_mode" not in columns:
            connection.execute(
                "ALTER TABLE jobs ADD COLUMN work_mode TEXT DEFAULT 'On-site'"
            )

        if "department" not in columns:
            connection.execute(
                "ALTER TABLE jobs ADD COLUMN department TEXT DEFAULT 'General'"
            )

        if "salary_min_lpa" not in columns:
            connection.execute(
                "ALTER TABLE jobs ADD COLUMN salary_min_lpa REAL DEFAULT 0"
            )

        if "salary_max_lpa" not in columns:
            connection.execute(
                "ALTER TABLE jobs ADD COLUMN salary_max_lpa REAL DEFAULT 0"
            )

        if "job_type" not in columns:
            connection.execute(
                "ALTER TABLE jobs ADD COLUMN job_type TEXT DEFAULT 'Full-time'"
            )

        if "is_synthetic" not in columns:
            connection.execute(
                "ALTER TABLE jobs ADD COLUMN is_synthetic INTEGER DEFAULT 0"
            )


def generate_sample_jobs(target_count=TARGET_JOB_COUNT):
    rng = random.Random(RANDOM_SEED)

    with get_connection() as connection:
        # Preserve all existing jobs. Generate only the missing amount.
        existing_count = connection.execute(
            "SELECT COUNT(*) FROM jobs"
        ).fetchone()[0]

        jobs_needed = max(0, target_count - existing_count)

        if jobs_needed == 0:
            print(f"Database already has {existing_count} jobs.")
            return

        existing_keys = {
            (
                row["title"],
                row["company"],
                row["location"],
                row["experience_level"],
            )
            for row in connection.execute(
                "SELECT title, company, location, experience_level FROM jobs"
            )
        }

        new_jobs = []
        attempts = 0
        max_attempts = jobs_needed * 10

        while len(new_jobs) < jobs_needed and attempts < max_attempts:
            attempts += 1

            role = rng.choice(ROLE_TEMPLATES)
            company = rng.choice(COMPANIES)
            location = rng.choice(LOCATIONS)
            experience = rng.choice(EXPERIENCE_LEVELS)
            work_mode = rng.choice(WORK_MODES)

            # Vary the skills while retaining role-relevant requirements.
            core_skills = role["skills"]
            required_count = rng.randint(
                min(3, len(core_skills)),
                min(6, len(core_skills)),
            )
            selected_skills = sorted(
                rng.sample(core_skills, required_count)
            )

            key = (
                role["title"],
                company,
                location,
                experience,
            )

            if key in existing_keys:
                continue

            existing_keys.add(key)

            if experience == "Internship":
                salary_min = rng.randint(1, 4) / 10
                salary_max = round(salary_min + rng.randint(1, 3) / 10, 2)
                job_type = "Internship"
            elif experience == "Fresher":
                salary_min = rng.randint(3, 6)
                salary_max = salary_min + rng.randint(1, 4)
                job_type = "Full-time"
            else:
                years = int(experience.split()[0].split("-")[0].replace("+", ""))
                salary_min = max(4, years * 2 + rng.randint(0, 3))
                salary_max = salary_min + rng.randint(3, 8)
                job_type = "Full-time"

            description = (
                f"{rng.choice(DESCRIPTIONS)} "
                f"This {role['title']} role focuses on "
                f"{role['department'].lower()}."
            )

            new_jobs.append((
                role["title"],
                company,
                location,
                ", ".join(selected_skills),
                experience,
                description,
                work_mode,
                role["department"],
                salary_min,
                salary_max,
                job_type,
                1,
            ))

        connection.executemany("""
            INSERT INTO jobs (
                title, company, location, required_skills,
                experience_level, description, work_mode,
                department, salary_min_lpa, salary_max_lpa,
                job_type, is_synthetic
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, new_jobs)

        total = connection.execute(
            "SELECT COUNT(*) FROM jobs"
        ).fetchone()[0]

        print(f"Added {len(new_jobs)} sample jobs.")
        print(f"Total jobs in database: {total}")


def get_all_jobs():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM jobs ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]


if __name__ == "__main__":
    initialize_database()
    generate_sample_jobs()

    jobs = get_all_jobs()
    print(f"Database location: {DB_PATH}")
    print(f"Jobs available: {len(jobs)}")
    print("Sample listing:")
    if jobs:
        print(jobs[0])
