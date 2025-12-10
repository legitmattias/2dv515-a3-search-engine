<script>
  let { results, count, searchTime } = $props();
</script>

{#if results && results.length > 0}
  <table>
    <thead>
      <tr>
        <th class="link-col">Link</th>
        <th>Score</th>
        <th>Content</th>
        <th>Location</th>
        <th>PageRank</th>
      </tr>
    </thead>
    <tbody>
      {#each results as result}
        <tr>
          <td class="link-col">{result.page}</td>
          <td>{result.score.toFixed(2)}</td>
          <td>{result.content.toFixed(2)}</td>
          <td>{result.location.toFixed(2)}</td>
          <td>{result.pagerank.toFixed(2)}</td>
        </tr>
      {/each}
    </tbody>
  </table>
  <p class="found-text">Found {count} results in {searchTime} sec</p>
{:else}
  <p class="no-results">No results found.</p>
{/if}

<style>
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
  }

  th, td {
    padding: 0.5rem;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }

  th {
    background: #808080;
    color: white;
  }

  .link-col {
    width: 50%;
  }

  .no-results {
    color: #666;
    font-style: italic;
    margin-top: 1rem;
  }

  .found-text {
    margin-top: 1rem;
    color: #666;
  }
</style>
