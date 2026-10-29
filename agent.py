
from matching import rank_jobs


def run_job_search_agent(
    candidate_skills,
    jobs,
    experience_level=None,
    preferred_location=None,
    top_n=10,
):
    """Rank jobs and provide skill-based recommendations."""

    if isinstance(candidate_skills, str):
        candidate_skills = [
            skill.strip()
            for skill in candidate_skills.split(",")
            if skill.strip()
        ]

    ranked_jobs = rank_jobs(
        candidate_skills,
        jobs,
        experience_level=experience_level,
    )

    if preferred_location and preferred_location.strip():
        location = preferred_location.strip().lower()

        location_matches = [
            job for job in ranked_jobs
            if location in str(job.get("location", "")).lower()
        ]

        if location_matches:
            ranked_jobs = location_matches

    recommendations = []

    for job in ranked_jobs[:top_n]:
        job_copy = dict(job)
        missing = job_copy.get("missing_skills", [])

        job_copy["agent_advice"] = (
            "Consider learning: " + ", ".join(missing)
            if missing
            else "Your listed skills match this job's requirements."
        )

        recommendations.append(job_copy)

    return {
        "agent": "SMART HIRE",
        "candidate_skills": candidate_skills,
        "jobs_analyzed": len(ranked_jobs),
        "recommendations": recommendations,
        "next_steps": [
            "Review the highest-ranked jobs.",
            "Identify and learn missing skills.",
            "Save suitable jobs to track applications.",
        ],
    }
