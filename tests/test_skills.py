from cv_matcher.services.skills import extract_skills


def test_extract_skills_finds_known_skills() -> None:
    text = "Wir suchen jemanden mit Python, FastAPI und Docker-Erfahrung."

    skills = extract_skills(text)

    assert skills == {"Python", "FastAPI", "Docker"}


def test_extract_skills_is_case_insensitive() -> None:
    text = "python UND docker kenntnisse"

    skills = extract_skills(text)

    assert skills == {"Python", "Docker"}


def test_extract_skills_respects_word_boundaries() -> None:
    text = "Wir nutzen Google Cloud und suchen jemanden mit JavaScript-Erfahrung."

    skills = extract_skills(text)

    assert "Go" not in skills
    assert "Java" not in skills


def test_extract_skills_returns_empty_set_for_no_matches() -> None:
    assert extract_skills("Wir suchen einen erfahrenen Koch.") == set()
