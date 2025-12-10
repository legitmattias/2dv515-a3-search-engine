"""FastAPI application for Wikipedia search engine."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.data_loader import load_pages
from app.pagerank import compute_pagerank
from app.search import search


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Load Wikipedia data and compute PageRank on startup."""
    data_dir = Path(__file__).parent.parent / 'data' / 'wikipedia'
    db = load_pages(data_dir)
    print(f"Loaded {len(db.pages)} pages with {len(db.word_to_pages)} unique words")
    compute_pagerank(db, iterations=20)
    print("PageRank computed (20 iterations)")
    application.state.db = db
    yield


app = FastAPI(title="Wikipedia Search Engine", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Wikipedia Search Engine API"}


@app.get("/api/search")
async def search_pages(
    q: str = Query(..., min_length=1, description="Search query")
):
    """
    Search Wikipedia pages.

    Returns top 5 pages ranked by:
    word_frequency + 0.8 * document_location + 0.5 * pagerank
    """
    db = app.state.db
    results = search(q, db, limit=5)

    return {
        "query": q,
        "results": [
            {
                "page": r.name,
                "score": r.score,
                "content": r.content_score,
                "location": round(0.8 * r.location_score, 2),
                "pagerank": round(0.5 * r.pagerank_score, 2)
            }
            for r in results
        ],
        "count": len(results)
    }
