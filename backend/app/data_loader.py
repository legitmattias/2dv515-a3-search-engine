"""Load Wikipedia pages and build search index."""

from dataclasses import dataclass, field
from pathlib import Path
from collections import Counter


@dataclass
class Page:
    """A Wikipedia page with its word and link data."""
    name: str
    category: str
    words: list[str]
    word_counts: Counter = field(default_factory=Counter)
    links: set[str] = field(default_factory=set)
    pagerank: float = 1.0


@dataclass
class PageDB:
    """Database of all indexed pages."""
    pages: list[Page]
    word_to_pages: dict[str, list[int]]
    name_to_index: dict[str, int] = field(default_factory=dict)


def load_pages(data_dir: Path) -> PageDB:
    """
    Load all Wikipedia pages from Words and Links directories.

    Args:
        data_dir: Path to wikipedia folder containing Words/ and Links/

    Returns:
        PageDB with pages, word-to-page index, and name-to-index mapping
    """
    pages = []
    word_to_pages: dict[str, set[int]] = {}
    name_to_index: dict[str, int] = {}

    words_dir = data_dir / "Words"
    links_dir = data_dir / "Links"

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

            # Load links for this page
            links_file = links_dir / category / name
            links: set[str] = set()
            if links_file.exists():
                links_content = links_file.read_text(encoding='utf-8')
                for line in links_content.strip().split('\n'):
                    if line.startswith('/wiki/'):
                        link_name = line[6:]  # Remove '/wiki/' prefix
                        if link_name != name:  # Exclude self-links
                            links.add(link_name)

            page = Page(
                name=name,
                category=category,
                words=words,
                word_counts=word_counts,
                links=links
            )
            pages.append(page)
            name_to_index[name] = page_idx

            for word in word_counts:
                if word not in word_to_pages:
                    word_to_pages[word] = set()
                word_to_pages[word].add(page_idx)

    # Convert sets to sorted lists
    word_to_pages_list = {
        w: sorted(indices) for w, indices in word_to_pages.items()
    }

    return PageDB(
        pages=pages,
        word_to_pages=word_to_pages_list,
        name_to_index=name_to_index
    )
