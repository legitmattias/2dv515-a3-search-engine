<script>
  import SearchResults from './lib/SearchResults.svelte';
  import { search } from './lib/api.js';

  let query = $state('');
  let results = $state(null);
  let count = $state(0);
  let searchTime = $state(0);
  let loading = $state(false);
  let error = $state('');

  async function handleSearch(event) {
    event.preventDefault();

    const trimmed = query.trim();
    if (!trimmed) return;

    loading = true;
    error = '';
    results = null;

    const startTime = performance.now();

    try {
      const response = await search(trimmed);
      const endTime = performance.now();

      results = response.results;
      count = response.count;
      searchTime = ((endTime - startTime) / 1000).toFixed(3);
    } catch (err) {
      error = 'Search failed. Please try again.';
      console.error(err);
    } finally {
      loading = false;
    }
  }
</script>

<main>
  <h1>Wikipedia Search Engine</h1>

  <form onsubmit={handleSearch}>
    <label for="search-input">Search query:</label>
    <input
      id="search-input"
      type="text"
      bind:value={query}
      disabled={loading}
    />
    <button type="submit" disabled={loading || !query.trim()}>
      Search
    </button>
  </form>

  {#if error}
    <p class="error">{error}</p>
  {/if}

  {#if results !== null}
    <SearchResults {results} {count} {searchTime} />
  {/if}
</main>

<style>
  main {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
  }

  h1 {
    margin-bottom: 1.5rem;
  }

  form {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  label {
    font-weight: 500;
  }

  input {
    padding: 0.5rem;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 300px;
  }

  button {
    padding: 0.5rem 1rem;
    background: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
  }

  button:hover:not(:disabled) {
    background: #e0e0e0;
  }

  button:disabled {
    cursor: not-allowed;
    opacity: 0.6;
  }

  .error {
    color: #d32f2f;
    padding: 0.5rem;
    background: #ffebee;
    border-radius: 4px;
  }
</style>
