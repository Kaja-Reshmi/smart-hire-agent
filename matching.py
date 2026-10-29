
# Skills that are related, but not identical.
RELATED_SKILLS = {
    "scikit-learn": {"machine learning"},
    "tensorflow": {"deep learning"},
    "pytorch": {"deep learning"},
    "keras": {"deep learning", "tensorflow"},
    "natural language processing": {"nlp"},
    "opencv": {"computer vision"},
    "power bi": {"data visualization", "data analysis"},
    "tableau": {"data visualization", "data analysis"},
    "pandas": {"data analysis"},
    "numpy": {"data analysis"},
}


def normalize_skills(skills):
    """Convert a comma-separated string or list to normalized skills."""
    if isinstance(skills, str):
        skills = skills.split(",")

    return {
        skill.strip().lower()
        for skill in skills
        if isinstance(skill, str) and skill.strip()
    }


def calculate_job_match(candidate_skills, required_skills):
    """Calculate a transparent skill-match score."""
    candidate = normalize_skills(candidate_skills)
    required = normalize_skills(required_skills)

    if not required:
        return {
            "match_percentage": 0.0,
            "matched_skills": [],
            "related_skills": [],
            "missing_skills": [],
        }

    matched = candidate & required
    related_matches = set()

    for candidate_skill in candidate:
        for related_skill in RELATED_SKILLS.get(candidate_skill, set()):
            if related_skill in required and related_skill not in matched:
                related_matches.add(related_skill)

    missing = required - matched - related_matches

    score = (
        len(matched) + 0.5 * len(related_matches)
    ) / len(required) * 100

    return {
        "match_percentage": round(score, 2),
        "matched_skills": sorted(matched),
        "related_skills": sorted(related_matches),
        "missing_skills": sorted(missing),
    }


def rank_jobs(
    candidate_skills,
    jobs,
    experience_level=None,
    preferred_location=None,
):
    """Rank jobs using skills, experience, and location preferences."""

    # Normalize candidate skills once instead of for every job.
    candidate = normalize_skills(candidate_skills)
    ranked_jobs = []

    experience_preference = (
        experience_level.strip().lower()
        if isinstance(experience_level, str) and experience_level.strip()
        else None
    )

    location_preference = (
        preferred_location.strip().lower()
        if isinstance(preferred_location, str) and preferred_location.strip()
        else None
    )

    for job in jobs:
        result = calculate_job_match(
            candidate,
            job.get("required_skills", ""),
        )

        job_experience = str(
            job.get("experience_level", "")
        ).strip().lower()

        job_location = str(
            job.get("location", "")
        ).strip().lower()

        experience_match = None
        if experience_preference:
            experience_match = (
                experience_preference == job_experience
            )

        location_match = None
        if location_preference:
            location_match = (
                location_preference in job_location
                or job_location == "remote"
            )

        ranking_score = result["match_percentage"]

        if experience_match is True:
            ranking_score += 10

        if location_match is True:
            ranking_score += 5

        ranked_jobs.append({
            **job,
            **result,
            "experience_match": experience_match,
            "location_match": location_match,
            "ranking_score": round(ranking_score, 2),
        })

    ranked_jobs.sort(
        key=lambda job: (
            job["ranking_score"],
            job["match_percentage"],
        ),
        reverse=True,
    )

    return ranked_jobs
