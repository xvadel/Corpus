<script>
  import { fade } from 'svelte/transition';

  export let track = null;
  export let onNavigate = (screen) => {};
  export let onBackToOnboarding = () => {};
</script>

<div class="dashboard-container" in:fade={{ duration: 300 }}>
  <!-- Top Bar -->
  <div class="top-bar">
    <div class="user-info">
      <span class="welcome-text">Hello, Learner 👋</span>
      <h1 class="track-title">{track.name}</h1>
    </div>
    <button class="switch-btn glass" on:click={onBackToOnboarding} title="Change track">
      <span class="material-icons-round switch-icon" style="color: {track.accentColor}">swap_horiz</span>
    </button>
  </div>

  <!-- Stats Row -->
  <div class="stats-row">
    <div class="stat-tile glass">
      <span class="material-icons-round stat-icon" style="color: {track.accentColor}">menu_book</span>
      <span class="stat-value">{track.sampleVocabulary.length}</span>
      <span class="stat-label">Words</span>
    </div>
    <div class="stat-tile glass">
      <span class="material-icons-round stat-icon" style="color: #FF6B6B">local_fire_department</span>
      <span class="stat-value">1 🔥</span>
      <span class="stat-label">Streak</span>
    </div>
    <div class="stat-tile glass">
      <span class="material-icons-round stat-icon" style="color: #00D09C">emoji_events</span>
      <span class="stat-value">Starter</span>
      <span class="stat-label">Level</span>
    </div>
  </div>

  <!-- Quick Actions -->
  <div class="section-title-row">
    <h2 class="section-title">Continue Learning</h2>
  </div>

  <div class="actions-list">
    <!-- Vocabulary -->
    <button class="action-card glass" style="--card-accent: {track.accentColor}" on:click={() => onNavigate('vocabulary')}>
      <div class="action-icon-wrapper" style="background: rgba(255, 255, 255, 0.05)">
        <span class="material-icons-round action-icon" style="color: {track.accentColor}">style</span>
      </div>
      <div class="action-info">
        <h3 class="action-name">Practice Vocabulary</h3>
        <p class="action-desc">Master {track.sampleVocabulary.length} key terms in your field</p>
      </div>
      <span class="material-icons-round arrow-icon">chevron_right</span>
    </button>

    <!-- Pitch Simulator -->
    <button class="action-card glass" style="--card-accent: #FF6B6B" on:click={() => onNavigate('chat')}>
      <div class="action-icon-wrapper" style="background: rgba(255, 255, 255, 0.05)">
        <span class="material-icons-round action-icon" style="color: #FF6B6B">record_voice_over</span>
      </div>
      <div class="action-info">
        <h3 class="action-name">Pitch Simulator</h3>
        <p class="action-desc">Roleplay a live conversation with an AI coach</p>
      </div>
      <span class="material-icons-round arrow-icon">chevron_right</span>
    </button>

    <!-- Grammar Coach -->
    <div class="action-card glass disabled" style="--card-accent: #00D09C">
      <div class="action-icon-wrapper" style="background: rgba(255, 255, 255, 0.02)">
        <span class="material-icons-round action-icon" style="color: #00D09C; opacity: 0.5;">spellcheck</span>
      </div>
      <div class="action-info">
        <h3 class="action-name">
          Grammar Coach <span class="badge-soon">Soon</span>
        </h3>
        <p class="action-desc">Get real-time corrections on your professional writing</p>
      </div>
    </div>
  </div>

  <!-- Focus Areas -->
  <div class="section-title-row">
    <h2 class="section-title">Your Focus Areas</h2>
  </div>

  <div class="focus-areas-wrap">
    {#each track.focusAreas as area}
      <div class="focus-badge" style="--badge-accent: {track.accentColor}">
        <span class="material-icons-round check-icon">check_circle</span>
        <span class="focus-text">{area}</span>
      </div>
    {/each}
  </div>
</div>

<style>
  .dashboard-container {
    max-width: 600px;
    width: 100%;
    margin: 0 auto;
    padding: 32px 24px;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    animation: fadeIn 0.4s ease-out;
  }

  .top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
  }

  .welcome-text {
    font-size: 14px;
    color: var(--text-secondary);
  }

  .track-title {
    font-size: 24px;
    font-weight: 600;
    margin-top: 4px;
  }

  .switch-btn {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    background: rgba(255, 255, 255, 0.04);
    transition: all 0.2s ease;
  }

  .switch-btn:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: scale(1.05);
  }

  .switch-icon {
    font-size: 24px;
  }

  .stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 32px;
  }

  .stat-tile {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px;
    background: rgba(255, 255, 255, 0.03);
    text-align: center;
  }

  .stat-icon {
    font-size: 22px;
    margin-bottom: 8px;
  }

  .stat-value {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 2px;
  }

  .stat-label {
    font-size: 12px;
    color: var(--text-muted);
  }

  .section-title-row {
    margin-bottom: 16px;
  }

  .section-title {
    font-size: 18px;
    font-weight: 600;
  }

  .actions-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 32px;
  }

  .action-card {
    display: flex;
    align-items: center;
    padding: 18px;
    text-align: left;
    width: 100%;
    cursor: pointer;
    background: rgba(255, 255, 255, 0.04);
    border-color: rgba(255, 255, 255, 0.08);
    transition: all 0.3s ease;
  }

  .action-card:not(.disabled):hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.15);
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  }

  .action-card.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .action-icon-wrapper {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 14px;
    border: 1px solid rgba(255, 255, 255, 0.05);
  }

  .action-icon {
    font-size: 24px;
  }

  .action-info {
    flex-grow: 1;
  }

  .action-name {
    font-size: 14px;
    font-weight: 600;
    color: white;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .badge-soon {
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.12);
    color: var(--text-secondary);
    font-weight: normal;
  }

  .action-desc {
    font-size: 12px;
    color: var(--text-secondary);
    line-height: 1.4;
  }

  .arrow-icon {
    font-size: 18px;
    color: var(--text-muted);
    transition: transform 0.2s ease, color 0.2s ease;
  }

  .action-card:hover .arrow-icon {
    color: white;
    transform: translateX(2px);
  }

  .focus-areas-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }

  .focus-badge {
    display: flex;
    align-items: center;
    padding: 10px 16px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    transition: all 0.3s ease;
  }

  .focus-badge:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: var(--badge-accent);
  }

  .check-icon {
    font-size: 16px;
    color: var(--badge-accent);
    margin-right: 8px;
  }

  .focus-text {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-primary);
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(8px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>
