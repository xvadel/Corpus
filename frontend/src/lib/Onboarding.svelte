<script>
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';

  export let onSelectTrack = (track) => {};

  let allTracks = [];
  let loading = true;
  let error = null;

  onMount(async () => {
    try {
      const res = await fetch('/api/vocabulary/tracks');
      if (!res.ok) throw new Error('Failed to load tracks from the server.');
      allTracks = await res.json();
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  });
</script>

<div class="onboarding-container" in:fade={{ duration: 300 }}>
  <div class="header">
    <h1 class="title">Welcome to Corpus 👋</h1>
    <h2 class="subtitle">What do you need to master?</h2>
    <p class="description">
      Choose your career track and we'll build your personalized vocabulary, grammar drills, and roleplay simulations.
    </p>
  </div>

  {#if loading}
    <div class="loading-container">
      <div class="spinner"></div>
      <p>Loading career tracks...</p>
    </div>
  {:else if error}
    <div class="error-container">
      <span class="material-icons-round error-icon">error_outline</span>
      <p>{error}</p>
      <button class="retry-btn glass" on:click={() => location.reload()}>Retry</button>
    </div>
  {:else}
    <div class="tracks-list">
      {#each allTracks as track, index}
        <button 
          class="track-card glass"
          style="--accent-color: {track.accentColor}; animation-delay: {index * 150}ms"
          on:click={() => onSelectTrack(track)}
        >
          <div class="card-left">
            <div class="icon-wrapper">
              <span class="material-icons-round track-icon">
                {track.icon === 'rocket' ? 'rocket_launch' : track.icon === 'code' ? 'code' : 'business_center'}
              </span>
            </div>
          </div>
          <div class="card-right">
            <h3 class="track-name">{track.name}</h3>
            <p class="track-desc">{track.description}</p>
            <div class="focus-areas-row">
              {#each track.focusAreas as area}
                <span class="focus-badge">{area}</span>
              {/each}
            </div>
          </div>
          <span class="material-icons-round arrow-icon">arrow_forward_ios</span>
        </button>
      {/each}
    </div>
  {/if}

  <p class="footer-note">You can always change your track later</p>
</div>

<style>
  .onboarding-container {
    max-width: 600px;
    width: 100%;
    margin: 0 auto;
    padding: 40px 24px;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    box-sizing: border-box;
  }

  .header {
    margin-top: 20px;
    margin-bottom: 32px;
  }

  .title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 8px;
    background: linear-gradient(135deg, #ffffff 0%, #a0a3bd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .subtitle {
    font-size: 20px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 12px;
  }

  .description {
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.6;
  }

  .tracks-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
    flex-grow: 1;
  }

  .track-card {
    display: flex;
    align-items: center;
    text-align: left;
    padding: 20px;
    cursor: pointer;
    width: 100%;
    background: rgba(255, 255, 255, 0.04);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
  }

  .track-card:hover {
    background: rgba(255, 255, 255, 0.08);
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    border-color: rgba(255, 255, 255, 0.16);
  }

  .track-card::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: var(--accent-color);
    opacity: 0.8;
  }

  .icon-wrapper {
    width: 52px;
    height: 52px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.05);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 18px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    transition: all 0.3s ease;
  }

  .track-card:hover .icon-wrapper {
    background: var(--accent-color);
    color: white;
    box-shadow: 0 0 15px var(--accent-color);
    border-color: transparent;
  }

  .track-icon {
    font-size: 24px;
    color: var(--accent-color);
    transition: color 0.3s ease;
  }

  .track-card:hover .track-icon {
    color: white;
  }

  .card-right {
    flex-grow: 1;
    padding-right: 12px;
  }

  .track-name {
    font-size: 18px;
    font-weight: 600;
    color: white;
    margin-bottom: 6px;
  }

  .track-desc {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.5;
    margin-bottom: 12px;
  }

  .focus-areas-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }

  .focus-badge {
    font-size: 11px;
    padding: 3px 8px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.05);
    color: var(--text-secondary);
    border: 1px solid rgba(255, 255, 255, 0.06);
  }

  .arrow-icon {
    font-size: 16px;
    color: var(--text-muted);
    transition: transform 0.3s ease, color 0.3s ease;
  }

  .track-card:hover .arrow-icon {
    color: white;
    transform: translateX(4px);
  }

  .footer-note {
    text-align: center;
    font-size: 12px;
    color: var(--text-muted);
    font-style: italic;
    margin-top: 32px;
    margin-bottom: 10px;
    animation: fadeIn 0.8s ease-out 1s both;
  }

  @keyframes slideUp {
    0% {
      opacity: 0;
      transform: translateY(20px);
    }
    100% {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes fadeIn {
    to {
      opacity: 1;
    }
  }

  .loading-container, .error-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex-grow: 1;
    padding: 40px 20px;
    text-align: center;
    color: var(--text-secondary);
    gap: 16px;
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.05);
    border-top: 3px solid #6c63ff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  .error-icon {
    font-size: 48px;
    color: #FF6B6B;
  }

  .retry-btn {
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.05);
    color: white;
    padding: 8px 24px;
    border-radius: 12px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s ease;
  }

  .retry-btn:hover {
    background: rgba(255, 255, 255, 0.1);
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
</style>
