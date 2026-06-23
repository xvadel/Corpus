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

<div class="onboarding-page" in:fade={{ duration: 250 }}>
  <!-- Top Navigation Bar -->
  <header class="navbar">
    <div class="navbar-left">
      <div class="logo-wrapper">
        <img src="/corpus_horizontal_logo.svg" alt="Corpus Logo" class="nav-logo" />
      </div>
    </div>
    <div class="navbar-center">
      <span class="nav-link active">Get Started</span>
      <span class="nav-link disabled">Dashboard</span>
      <span class="nav-link disabled">Learning</span>
      <span class="nav-link disabled">Simulator</span>
    </div>
    <div class="navbar-right">
      <button class="upgrade-btn">Upgrade</button>
      <button class="new-project-btn">Request Demo</button>
      <span class="material-icons-round nav-icon">notifications</span>
      <span class="material-icons-round nav-icon">settings</span>
      <div class="avatar">
        <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=100&q=80" alt="Avatar" />
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="hero-section">
    <div class="hero-container">
      <span class="badge">NEXT-GEN PROFESSIONAL EDUCATION</span>
      <h1 class="hero-title">Communication,<br/>Powered by Your Projects.</h1>
      <p class="hero-subtitle">
        Corpus transforms technical output into high-impact communication. No more generic templates—select a specialized domain to master the language of leadership.
      </p>
    </div>
  </section>

  <!-- Main Tracks Container -->
  <main class="main-content">
    <h2 class="section-title">Select Your Career Track</h2>
    <p class="section-desc">Choose a domain to build your personalized terminology catalog, GapAnalyzer prerequisites, and Investor roleplays.</p>

    {#if loading}
      <div class="loading-state">
        <div class="spinner"></div>
        <p>Analyzing available curricula...</p>
      </div>
    {:else if error}
      <div class="error-state">
        <span class="material-icons-round error-icon">error_outline</span>
        <p class="error-text">{error}</p>
        <button class="retry-btn" on:click={() => location.reload()}>Retry Connection</button>
      </div>
    {:else}
      <div class="tracks-grid">
        {#each allTracks as track}
          <button class="track-card" on:click={() => onSelectTrack(track)}>
            <div class="track-card-header" style="--accent: {track.accentColor || '#6C63FF'}">
              <div class="track-icon-box">
                <span class="material-icons-round">
                  {track.icon === 'rocket' ? 'rocket_launch' : track.icon === 'code' ? 'code' : track.icon === 'briefcase' ? 'business_center' : 'psychology'}
                </span>
              </div>
              <h3 class="track-name">{track.name}</h3>
            </div>
            <p class="track-description">{track.description}</p>
            
            <div class="focus-badges">
              {#each track.focusAreas || [] as area}
                <span class="badge-item">{area}</span>
              {/each}
            </div>

            <div class="card-footer">
              <span class="term-count">{track.term_count || 8} Active Concepts</span>
              <span class="start-text">Start Onboarding <span class="material-icons-round">arrow_forward</span></span>
            </div>
          </button>
        {/each}
      </div>
    {/if}
  </main>

  <!-- Paradigm Shift Section -->
  <section class="comparison-section">
    <h2 class="comparison-title">A Paradigm Shift in Growth</h2>
    <p class="comparison-subtitle">We're evolving from static tracks to dynamic, project-aware intelligence.</p>

    <div class="comparison-grid">
      <div class="comparison-card legacy">
        <div class="card-type">THE LEGACY</div>
        <h3>Original Vision</h3>
        <p>Linear, track-based learning focusing on theoretical exercises and standardized curriculum paths.</p>
        <ul class="comparison-list">
          <li class="fail"><span class="material-icons-round">close</span> Static Skill Paths</li>
          <li class="fail"><span class="material-icons-round">close</span> Hypothetical Scenarios</li>
          <li class="fail"><span class="material-icons-round">close</span> Manual Integration</li>
        </ul>
      </div>

      <div class="comparison-card future">
        <div class="card-type">THE FUTURE</div>
        <h3>New Vision</h3>
        <p>Project-aware AI that maps your actual work to communication excellence, learning in real-time from your repository.</p>
        <ul class="comparison-list">
          <li class="success"><span class="material-icons-round">check_circle</span> Real-time Repository Sync</li>
          <li class="success"><span class="material-icons-round">check_circle</span> Contextual Narrative Generation</li>
          <li class="success"><span class="material-icons-round">check_circle</span> Integrated Simulator Testing</li>
        </ul>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="footer">
    <div class="footer-left">
      <img src="/corpus_horizontal_logo.svg" alt="Corpus Logo" class="footer-logo" />
      <p class="copyright">© 2026 Corpus AI. Knowledge & Impact.</p>
    </div>
    <div class="footer-right">
      <span class="footer-link">Privacy Policy</span>
      <span class="footer-link">Terms of Service</span>
      <span class="footer-link">API Docs</span>
      <span class="footer-link">Careers</span>
    </div>
  </footer>
</div>

<style>
  .onboarding-page {
    background-color: var(--bg-light-main);
    color: var(--text-light-primary);
    min-height: 100vh;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  /* Top Navigation Bar */
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    max-width: 1200px;
    height: 70px;
    padding: 0 24px;
    border-bottom: 1px solid var(--border-light);
    background-color: var(--bg-light-card);
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .nav-logo {
    height: 36px;
    color: var(--text-light-primary);
  }

  .navbar-center {
    display: flex;
    gap: 24px;
  }

  .nav-link {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-light-secondary);
    cursor: pointer;
    position: relative;
    padding: 8px 0;
  }

  .nav-link.active {
    color: var(--text-light-primary);
    font-weight: 600;
  }

  .nav-link.active::after {
    content: '';
    position: absolute;
    bottom: -15px;
    left: 0;
    right: 0;
    height: 2px;
    background-color: var(--primary-accent);
  }

  .nav-link.disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .navbar-right {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .upgrade-btn {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-light-secondary);
    background: none;
    border: none;
    cursor: pointer;
  }

  .new-project-btn {
    font-size: 13px;
    font-weight: 600;
    color: white;
    background-color: var(--text-light-primary);
    border: none;
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .new-project-btn:hover {
    background-color: #334155;
  }

  .nav-icon {
    font-size: 20px;
    color: var(--text-light-secondary);
    cursor: pointer;
  }

  .avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    overflow: hidden;
    border: 1px solid var(--border-light);
  }

  .avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  /* Hero Section */
  .hero-section {
    width: 100%;
    background-color: #0F172A; /* Premium Dark Hero Banner */
    color: white;
    padding: 80px 24px;
    display: flex;
    justify-content: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }

  .hero-container {
    max-width: 800px;
    width: 100%;
    text-align: center;
  }

  .badge {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #38BDF8;
    background-color: rgba(56, 189, 248, 0.12);
    padding: 4px 10px;
    border-radius: 20px;
    display: inline-block;
    margin-bottom: 24px;
  }

  .hero-title {
    font-size: 48px;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 20px;
    letter-spacing: -1px;
  }

  .hero-subtitle {
    font-size: 16px;
    line-height: 1.6;
    color: #94A3B8;
    max-width: 650px;
    margin: 0 auto;
  }

  /* Main Tracks Content */
  .main-content {
    width: 100%;
    max-width: 1200px;
    padding: 80px 24px;
  }

  .section-title {
    font-size: 32px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 12px;
    letter-spacing: -0.5px;
  }

  .section-desc {
    font-size: 15px;
    color: var(--text-light-secondary);
    text-align: center;
    max-width: 600px;
    margin: 0 auto 50px auto;
  }

  .loading-state, .error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px;
    text-align: center;
    background: var(--bg-light-card);
    border: 1px solid var(--border-light);
    border-radius: 16px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  }

  .spinner {
    width: 32px;
    height: 32px;
    border: 3px solid var(--border-light);
    border-top: 3px solid var(--primary-accent);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-bottom: 16px;
  }

  .error-icon {
    font-size: 40px;
    color: var(--danger-red);
    margin-bottom: 12px;
  }

  .error-text {
    font-size: 14px;
    color: var(--text-light-secondary);
    margin-bottom: 16px;
  }

  .retry-btn {
    background-color: var(--text-light-primary);
    color: white;
    border: none;
    padding: 8px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
  }

  .tracks-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
  }

  .track-card {
    background-color: var(--bg-light-card);
    border: 1px solid var(--border-light);
    border-radius: 16px;
    padding: 28px;
    text-align: left;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 280px;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
  }

  .track-card:hover {
    transform: translateY(-4px);
    border-color: #CBD5E1;
    box-shadow: 0 12px 20px -3px rgba(0, 0, 0, 0.08);
  }

  .track-card-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 16px;
  }

  .track-icon-box {
    width: 44px;
    height: 44px;
    border-radius: 10px;
    background-color: rgba(108, 99, 255, 0.08);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--accent);
  }

  .track-icon-box span {
    font-size: 22px;
  }

  .track-name {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-light-primary);
    margin: 0;
  }

  .track-description {
    font-size: 13.5px;
    line-height: 1.5;
    color: var(--text-light-secondary);
    margin-bottom: 20px;
    flex-grow: 1;
  }

  .focus-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 24px;
  }

  .badge-item {
    font-size: 11px;
    background-color: #F1F5F9;
    color: var(--text-light-secondary);
    padding: 3px 8px;
    border-radius: 6px;
    font-weight: 500;
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid var(--border-light);
    padding-top: 16px;
  }

  .term-count {
    font-size: 12px;
    font-weight: 500;
    color: var(--text-light-muted);
  }

  .start-text {
    font-size: 13px;
    font-weight: 600;
    color: var(--primary-accent);
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .start-text span {
    font-size: 14px;
    transition: transform 0.2s;
  }

  .track-card:hover .start-text span {
    transform: translateX(3px);
  }

  /* Comparison Section */
  .comparison-section {
    width: 100%;
    max-width: 900px;
    padding: 60px 24px 80px 24px;
    border-top: 1px solid var(--border-light);
  }

  .comparison-title {
    font-size: 28px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 8px;
  }

  .comparison-subtitle {
    font-size: 14px;
    color: var(--text-light-secondary);
    text-align: center;
    margin-bottom: 44px;
  }

  .comparison-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }

  .comparison-card {
    background-color: var(--bg-light-card);
    border: 1px solid var(--border-light);
    border-radius: 16px;
    padding: 32px;
  }

  .comparison-card.future {
    background-color: #0F172A;
    color: white;
    border-color: #1E293B;
  }

  .card-type {
    font-size: 9.5px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: var(--text-light-muted);
    margin-bottom: 12px;
  }

  .future .card-type {
    color: #38BDF8;
  }

  .comparison-card h3 {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 8px;
  }

  .comparison-card p {
    font-size: 13.5px;
    line-height: 1.5;
    color: var(--text-light-secondary);
    margin-bottom: 24px;
  }

  .future p {
    color: #94A3B8;
  }

  .comparison-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .comparison-list li {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 600;
  }

  .comparison-list li span {
    font-size: 18px;
  }

  .comparison-list li.fail {
    color: var(--text-light-secondary);
  }

  .comparison-list li.fail span {
    color: var(--danger-red);
  }

  .comparison-list li.success {
    color: white;
  }

  .comparison-list li.success span {
    color: #38BDF8;
  }

  /* Footer */
  .footer {
    width: 100%;
    max-width: 1200px;
    padding: 40px 24px;
    border-top: 1px solid var(--border-light);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .footer-logo {
    height: 28px;
    margin-bottom: 8px;
    opacity: 0.8;
  }

  .copyright {
    font-size: 12px;
    color: var(--text-light-muted);
  }

  .footer-right {
    display: flex;
    gap: 20px;
  }

  .footer-link {
    font-size: 12px;
    font-weight: 500;
    color: var(--text-light-secondary);
    cursor: pointer;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }
</style>
