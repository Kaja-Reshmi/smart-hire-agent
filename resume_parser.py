
import re


# Starter skill dictionary. We can expand this later.
SKILL_KEYWORDS = [
    "python",
    "java",
    "sql",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "keras",
    "nlp",
    "natural language processing",
    "computer vision",
    "opencv",
    "excel",
    "power bi",
    "tableau",
    "fastapi",
    "flask",
    "django",
    "html",
    "css",
    "javascript",
    "react",
    "git",
    "docker",
    "aws",
    "azure",
    "statistics",
    "matplotlib",
    "seaborn",
    "communication",
    "problem solving",
]


def extract_skills(resume_text):
    """Extract known skills from résumé text."""
    text = resume_text.lower()
    found_skills = []

    for skill in SKILL_KEYWORDS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(set(found_skills))


def parse_resume_text(resume_text):
    """Return extracted skills and basic résumé statistics."""
    skills = extract_skills(resume_text)

    return {
        "skills_found": skills,
        "total_skills_found": len(skills),
    }
