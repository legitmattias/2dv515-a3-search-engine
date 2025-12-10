const API_BASE = 'http://localhost:8000';

export async function search(query) {
  const res = await fetch(`${API_BASE}/api/search?q=${encodeURIComponent(query)}`);
  if (!res.ok) {
    throw new Error('Search failed');
  }
  return res.json();
}
