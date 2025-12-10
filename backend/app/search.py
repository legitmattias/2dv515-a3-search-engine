"""Search functionality with word frequency ranking."""

from dataclasses import dataclass
from app.data_loader import PageDB


@dataclass
class SearchResult:
    """A single search result."""
    name: str
    score: float
    content_score: float


def search(query: str, db: PageDB, limit: int = 5) -> list[SearchResult]:
    """
    Search for a word and return top results ranked by word frequency.

    Scoring: frequency / max_frequency (normalized to 0.0-1.0)
    """
    word = query.lower().strip()

    if not word or word not in db.word_to_pages:
        return []

    page_indices = db.word_to_pages[word]

    # Get frequency for each page
    results = []
    for idx in page_indices:
        page = db.pages[idx]
        frequency = page.word_counts.get(word, 0)
        results.append((page.name, frequency))

    # Sort by frequency descending
    results.sort(key=lambda x: x[1], reverse=True)

    if not results:
        return []

    max_freq = results[0][1]

    return [
        SearchResult(
            name=name,
            score=round(freq / max_freq, 2),
            content_score=round(freq / max_freq, 2)
        )
        for name, freq in results[:limit]
    ]
