<script>
  import { fade } from 'svelte/transition';

  export let track = null;
  export let onNavigate = (screen) => {};
  export let onBackToOnboarding = () => {};
</script>

<div class="dashboard-page" in:fade={{ duration: 250 }}>
  <!-- Top Navigation Bar -->
  <header class="navbar">
    <div class="navbar-left">
      <div class="logo-wrapper">
        <img src="/corpus_horizontal_logo.svg" alt="Corpus Logo" class="nav-logo" />
      </div>
    </div>
    <div class="navbar-center">
      <span class="nav-link active" on:click={() => onNavigate('dashboard')}>Dashboard</span>
      <span class="nav-link" on:click={() => onNavigate('vocabulary')}>Learning</span>
      <span class="nav-link" on:click={() => onNavigate('chat')}>Simulator</span>
      <span class="nav-link disabled">GitHub Intel</span>
    </div>
    <div class="navbar-right">
      <button class="upgrade-btn" on:click={onBackToOnboarding}>Change Track</button>
      <button class="new-project-btn" on:click={() => onNavigate('chat')}>Launch Simulator</button>
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
      <div class="hero-left">
        <span class="badge">NEXT-GEN INTELLIGENCE</span>
        <h1 class="hero-title">Communication,<br/>Powered by {track.name}.</h1>
        <p class="hero-subtitle">
          Corpus extracts core lexicons and maps them to professional communication pipelines. Leverage your vocabulary bank to master client discussions and investor pitches.
        </p>
        <div class="hero-buttons">
          <button class="primary-btn" on:click={() => onNavigate('vocabulary')}>Explore Vocab</button>
          <button class="secondary-btn" on:click={() => onNavigate('chat')}>View Simulator</button>
        </div>
      </div>
      
      <!-- Right Side Status Card -->
      <div class="hero-right">
        <div class="status-card">
          <div class="status-header">
            <span class="status-title">Track Status</span>
            <span class="pulse-indicator"><span class="pulse-dot"></span> Active</span>
          </div>
          <h3 class="track-project">{track.name}</h3>
          <div class="progress-bar-container">
            <div class="progress-bar" style="width: 79%"></div>
          </div>
          <div class="progress-labels">
            <span>Knowledge Ingestion</span>
            <span>79% Complete</span>
          </div>
          
          <div class="metrics-grid">
            <div class="metric-item">
              <span class="metric-num">{track.sampleVocabulary.length}</span>
              <span class="metric-label">Technical Specs</span>
            </div>
            <div class="metric-item">
              <span class="metric-num">1.4k</span>
              <span class="metric-label">Prerequisites</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Main Section Grid -->
  <main class="main-layout">
    <!-- Left Panel: Core Stats & Focus Areas -->
    <div class="left-panel">
      <h2 class="panel-title">Track Progress</h2>
      
      <div class="stats-grid">
        <div class="stat-card">
          <span class="material-icons-round stat-icon text-purple">menu_book</span>
          <span class="stat-value">{track.sampleVocabulary.length}</span>
          <span class="stat-label">Indexed Terms</span>
        </div>
        <div class="stat-card">
          <span class="material-icons-round stat-icon text-red">local_fire_department</span>
          <span class="stat-value">1 🔥</span>
          <span class="stat-label">Daily Streak</span>
        </div>
        <div class="stat-card">
          <span class="material-icons-round stat-icon text-green">emoji_events</span>
          <span class="stat-value">Starter</span>
          <span class="stat-label">Curriculum Level</span>
        </div>
      </div>

      <h2 class="panel-title" style="margin-top: 40px;">Focus Areas</h2>
      <div class="focus-list">
        {#each track.focusAreas || [] as area}
          <div class="focus-item">
            <span class="material-icons-round check-icon">check_circle</span>
            <span>{area}</span>
          </div>
        {/each}
      </div>
    </div>

    <!-- Right Panel: Navigation / Practice Options -->
    <div class="right-panel">
      <h2 class="panel-title">Your Practice Center</h2>
      
      <div class="practice-cards">
        <!-- Vocab Practice Card -->
        <button class="practice-card" on:click={() => onNavigate('vocabulary')}>
          <div class="card-left">
            <span class="material-icons-round p-icon text-purple">style</span>
          </div>
          <div class="card-right">
            <h3>Interactive Vocabulary Deck</h3>
            <p>Study terms, definitions, and analogies curated for {track.name}.</p>
            <span class="go-link">Browse Cards <span class="material-icons-round">chevron_right</span></span>
          </div>
        </button>

        <!-- Chat Simulator Card -->
        <button class="practice-card" on:click={() => onNavigate('chat')}>
          <div class="card-left">
            <span class="material-icons-round p-icon text-red">forum</span>
          </div>
          <div class="card-right">
            <h3>AI Investor Simulator</h3>
            <p>Engage in a live, high-stakes conversational simulation with an AI partner.</p>
            <span class="go-link">Start Simulation <span class="material-icons-round">chevron_right</span></span>
          </div>
        </button>

        <!-- Analysis Engine Card -->
        <div class="practice-card disabled">
          <div class="card-left">
            <span class="material-icons-round p-icon text-green">analytics</span>
          </div>
          <div class="card-right">
            <h3>Project Speech Evaluator <span class="badge">Soon</span></h3>
            <p>Record your voice explaining your project to receive real-time clarity scores.</p>
          </div>
        </div>
      </div>
    </div>
  </main>

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
  .dashboard-page {
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

  /* Hero Banner */
  .hero-section {
    width: 100%;
    background-color: #0F172A; /* Premium Dark Navy Hero background */
    color: white;
    padding: 70px 24px;
    display: flex;
    justify-content: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }

  .hero-container {
    max-width: 1152px;
    width: 100%;
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 40px;
    align-items: center;
  }

  .badge {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #38BDF8;
    background-color: rgba(56, 189, 248, 0.12);
    padding: 4px 10px;
    border-radius: 20px;
    display: inline-block;
    margin-bottom: 20px;
  }

  .hero-title {
    font-size: 40px;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 16px;
    letter-spacing: -1px;
    color: white;
  }

  .hero-subtitle {
    font-size: 15px;
    line-height: 1.6;
    color: #94A3B8;
    max-width: 550px;
    margin-bottom: 28px;
  }

  .hero-buttons {
    display: flex;
    gap: 12px;
  }

  .primary-btn {
    background-color: white;
    color: var(--text-light-primary);
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 13.5px;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .primary-btn:hover {
    background-color: #E2E8F0;
  }

  .secondary-btn {
    background: none;
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 13.5px;
    cursor: pointer;
    transition: border-color 0.2s, background-color 0.2s;
  }

  .secondary-btn:hover {
    border-color: white;
    background-color: rgba(255, 255, 255, 0.05);
  }

  /* Status Card (Right Side) */
  .status-card {
    background-color: #1E293B;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px;
  }

  .status-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }

  .status-title {
    font-size: 11px;
    font-weight: 700;
    color: #38BDF8;
    letter-spacing: 1px;
  }

  .pulse-indicator {
    font-size: 11px;
    font-weight: 600;
    color: #10B981;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .pulse-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: #10B981;
    box-shadow: 0 0 8px #10B981;
  }

  .track-project {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 20px;
    color: white;
  }

  .progress-bar-container {
    height: 6px;
    background-color: #334155;
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 8px;
  }

  .progress-bar {
    height: 100%;
    background-color: #38BDF8;
    border-radius: 3px;
  }

  .progress-labels {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    font-weight: 600;
    color: #64748B;
    margin-bottom: 20px;
  }

  .metrics-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    border-top: 1px solid #334155;
    padding-top: 16px;
  }

  .metric-item {
    display: flex;
    flex-direction: column;
  }

  .metric-num {
    font-size: 18px;
    font-weight: 700;
    color: white;
  }

  .metric-label {
    font-size: 11px;
    color: #64748B;
    font-weight: 500;
  }

  /* Main Layout */
  .main-layout {
    width: 100%;
    max-width: 1152px;
    padding: 60px 24px;
    display: grid;
    grid-template-columns: 0.9fr 1.1fr;
    gap: 48px;
  }

  .panel-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 20px;
    letter-spacing: -0.3px;
  }

  /* Left Panel */
  .stats-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .stat-card {
    background-color: var(--bg-light-card);
    border: 1px solid var(--border-light);
    border-radius: 12px;
    padding: 18px;
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .stat-icon {
    font-size: 28px;
  }

  .text-purple { color: #8B5CF6; }
  .text-red { color: #EF4444; }
  .text-green { color: #10B981; }

  .stat-value {
    font-size: 20px;
    font-weight: 700;
    color: var(--text-light-primary);
  }

  .stat-label {
    font-size: 12px;
    color: var(--text-light-secondary);
    display: block;
    margin-top: 2px;
  }

  .focus-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .focus-item {
    display: flex;
    align-items: center;
    gap: 10px;
    background-color: var(--bg-light-card);
    border: 1px solid var(--border-light);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 13.5px;
    font-weight: 600;
  }

  .check-icon {
    color: #10B981;
    font-size: 18px;
  }

  /* Right Panel */
  .practice-cards {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .practice-card {
    background-color: var(--bg-light-card);
    border: 1px solid var(--border-light);
    border-radius: 14px;
    padding: 24px;
    display: flex;
    align-items: flex-start;
    gap: 20px;
    text-align: left;
    cursor: pointer;
    width: 100%;
    transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
  }

  .practice-card:hover:not(.disabled) {
    transform: translateY(-2px);
    border-color: #CBD5E1;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
  }

  .practice-card.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .p-icon {
    font-size: 32px;
  }

  .practice-card h3 {
    font-size: 16px;
    font-weight: 700;
    color: var(--text-light-primary);
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .practice-card h3 .badge {
    font-size: 9.5px;
    background-color: #E2E8F0;
    color: var(--text-light-secondary);
    padding: 2px 6px;
    border-radius: 4px;
    margin: 0;
    letter-spacing: normal;
  }

  .practice-card p {
    font-size: 13px;
    color: var(--text-light-secondary);
    line-height: 1.45;
    margin-bottom: 12px;
  }

  .go-link {
    font-size: 13px;
    font-weight: 600;
    color: var(--primary-accent);
    display: flex;
    align-items: center;
    gap: 2px;
  }

  .go-link span {
    font-size: 16px;
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
</style>
