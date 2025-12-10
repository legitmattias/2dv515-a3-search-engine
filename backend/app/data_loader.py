"""Load Wikipedia pages and build search index."""

from dataclasses import dataclass, field
from pathlib import Path
from collections import Counter


@dataclass
class Page:
    """A Wikipedia page with its word data."""
    name: str
    category: str
    words: list[str]
    word_counts: Counter = field(default_factory=Counter)


@dataclass
class PageDB:
    """Database of all indexed pages."""
    pages: list[Page]
    word_to_pages: dict[str, list[int]]


def load_pages(data_dir: Path) -> PageDB:
    """
    Load all Wikipedia pages from Words directory.

    Args:
        data_dir: Path to wikipedia folder containing Words/ and Links/

    Returns:
        PageDB with pages and word-to-page index
    """
    pages = []
    word_to_pages: dict[str, set[int]] = {}

    words_dir = data_dir / "Words"

    for category_dir in sorted(words_dir.iterdir()):
        if not category_dir.is_dir():
            continue
        category = category_dir.name

        for page_file in sorted(category_dir.iterdir()):
            page_idx = len(pages)
            name = page_file.name

            content = page_file.read_text(encoding='utf-8')
            words = content.split()

            word_counts = Counter(words)

            page = Page(
                name=name,
                category=category,
                words=words,
                word_counts=word_counts
            )
            pages.append(page)

            for word in word_counts:
                if word not in word_to_pages:
                    word_to_pages[word] = set()
                word_to_pages[word].add(page_idx)

    # Convert sets to sorted lists
    word_to_pages_list = {
        w: sorted(indices) for w, indices in word_to_pages.items()
    }

    return PageDB(pages=pages, word_to_pages=word_to_pages_list)
