"""Search functionality with word frequency and document location ranking."""

from dataclasses import dataclass
from app.data_loader import PageDB


@dataclass
class SearchResult:
    """A single search result."""
    name: str
    score: float
    content_score: float
    location_score: float


def get_word_frequency(page, words: list[str]) -> int:
    """Sum of frequencies for all query words in a page."""
    return sum(page.word_counts.get(word, 0) for word in words)


def get_document_location(page, words: list[str]) -> int:
    """
    Sum of first occurrence positions for all query words.
    Position is 1-indexed. If word not found, use 100000.
    """
    total = 0
    for word in words:
        try:
            pos = page.words.index(word) + 1  # 1-indexed
        except ValueError:
            pos = 100000  # Not found
        total += pos
    return total


def normalize_higher_better(scores: list[float]) -> list[float]:
    """Normalize scores where higher is better. Max becomes 1.0."""
    if not scores:
        return []
    max_val = max(scores)
    if max_val == 0:
        return [0.0] * len(scores)
    return [s / max_val for s in scores]


def normalize_lower_better(scores: list[float]) -> list[float]:
    """Normalize scores where lower is better. Min becomes 1.0."""
    if not scores:
        return []
    min_val = min(scores)
    return [min_val / max(s, 0.00001) for s in scores]


def search(query: str, db: PageDB, limit: int = 5) -> list[SearchResult]:
    """
    Search for words and return top results.

    Scoring: word_frequency + 0.8 * document_location
    Both metrics are normalized to 0.0-1.0 range.
    """
    words = query.lower().strip().split()

    if not words:
        return []

    # Find pages containing ANY of the query words (OR search)
    page_indices = set()
    for word in words:
        if word in db.word_to_pages:
            page_indices.update(db.word_to_pages[word])

    if not page_indices:
        return []

    # Calculate raw scores for each page
    raw_data = []
    for idx in page_indices:
        page = db.pages[idx]
        freq = get_word_frequency(page, words)
        loc = get_document_location(page, words)
        raw_data.append((page.name, freq, loc))

    # Extract raw scores
    freqs = [d[1] for d in raw_data]
    locs = [d[2] for d in raw_data]

    # Normalize
    norm_freqs = normalize_higher_better(freqs)
    norm_locs = normalize_lower_better(locs)

    # Combine scores and build results
    results = []
    for i, (name, _, _) in enumerate(raw_data):
        content = norm_freqs[i]
        location = norm_locs[i]
        score = content + 0.8 * location
        results.append(SearchResult(
            name=name,
            score=round(score, 2),
            content_score=round(content, 2),
            location_score=round(location, 2)
        ))

    # Sort by combined score descending
    results.sort(key=lambda x: x.score, reverse=True)

    return results[:limit]
