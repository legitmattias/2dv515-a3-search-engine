"""PageRank calculation."""

from app.data_loader import PageDB


def compute_pagerank(db: PageDB, iterations: int = 20, damping: float = 0.85):
    """
    Runs PageRank on all pages. Each page starts with rank 1.0 and the
    algorithm iterates until values stabilize (20 iterations should be
    enough for a dataset this size).
    """
    # Start everyone at 1.0
    for page in db.pages:
        page.pagerank = 1.0

    for _ in range(iterations):
        new_ranks = []

        for page in db.pages:
            # 0.15 base rank (random jump probability)
            rank = 1 - damping

            # Check which pages link to this one
            for other_page in db.pages:
                if page.name in other_page.links:
                    num_links = len(other_page.links)
                    if num_links > 0:
                        # Linking page shares its rank equally among all its outgoing links
                        rank += damping * (other_page.pagerank / num_links)

            new_ranks.append(rank)

        # Apply all updates after the iteration
        for i, page in enumerate(db.pages):
            page.pagerank = new_ranks[i]
