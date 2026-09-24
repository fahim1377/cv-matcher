from cv_matcher.services.embeddings import EMBEDDING_DIMENSIONS, embed_text


def test_embed_text_returns_vector_with_expected_dimensions() -> None:
    embedding = embed_text("Python-Entwickler mit FastAPI-Erfahrung")

    assert len(embedding) == EMBEDDING_DIMENSIONS
    assert all(isinstance(value, float) for value in embedding)


def test_similar_texts_are_closer_than_dissimilar_texts() -> None:
    def cosine_similarity(a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b, strict=True))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(y * y for y in b) ** 0.5
        return dot / (norm_a * norm_b)

    cv_text = "Erfahrener Python-Entwickler mit FastAPI und PostgreSQL"
    similar_job = "Gesucht: Python-Backend-Entwickler mit FastAPI-Kenntnissen"
    unrelated_job = "Gesucht: Koch fuer italienisches Restaurant in Berlin"

    cv_embedding = embed_text(cv_text)
    similar_embedding = embed_text(similar_job)
    unrelated_embedding = embed_text(unrelated_job)

    similar_score = cosine_similarity(cv_embedding, similar_embedding)
    unrelated_score = cosine_similarity(cv_embedding, unrelated_embedding)

    assert similar_score > unrelated_score
