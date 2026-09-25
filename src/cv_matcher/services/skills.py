import re

SKILL_KEYWORDS = (
    "Python",
    "FastAPI",
    "Django",
    "Flask",
    "Docker",
    "Kubernetes",
    "PostgreSQL",
    "MySQL",
    "SQL",
    "Redis",
    "Celery",
    "Machine Learning",
    "Deep Learning",
    "PyTorch",
    "TensorFlow",
    "scikit-learn",
    "NLP",
    "LLM",
    "RAG",
    "CI/CD",
    "GitHub Actions",
    "Git",
    "REST API",
    "Pytest",
    "Linux",
    "AWS",
    "Azure",
    "GCP",
    "Agile",
    "Scrum",
    "Java",
    "Go",
    "TypeScript",
    "React",
    "Pandas",
    "NumPy",
    "Spark",
    "Airflow",
)

_SKILL_PATTERNS = tuple(
    (skill, re.compile(rf"\b{re.escape(skill)}\b", re.IGNORECASE)) for skill in SKILL_KEYWORDS
)


def extract_skills(text: str) -> set[str]:
    return {skill for skill, pattern in _SKILL_PATTERNS if pattern.search(text)}
