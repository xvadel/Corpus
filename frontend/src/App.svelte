<script>
  import Splash from './lib/Splash.svelte';
  import Onboarding from './lib/Onboarding.svelte';
  import Dashboard from './lib/Dashboard.svelte';
  import Vocabulary from './lib/Vocabulary.svelte';
  import Chat from './lib/Chat.svelte';

  let currentScreen = 'splash'; // 'splash' | 'onboarding' | 'dashboard' | 'vocabulary' | 'chat'
  let selectedTrack = null;
  let isLoadingTrack = false;

  function handleSplashComplete() {
    currentScreen = 'onboarding';
  }

  async function handleSelectTrack(track) {
    isLoadingTrack = true;
    try {
      const res = await fetch(`/api/vocabulary/${track.id}`);
      if (!res.ok) throw new Error('Failed to fetch vocabulary terms');
      const data = await res.json();
      selectedTrack = {
        ...track,
        sampleVocabulary: data.terms || []
      };
      currentScreen = 'dashboard';
    } catch (err) {
      console.error("Error loading track terms, falling back:", err);
      selectedTrack = {
        ...track,
        sampleVocabulary: track.sampleVocabulary || []
      };
      currentScreen = 'dashboard';
    } finally {
      isLoadingTrack = false;
    }
  }

  function handleNavigate(screen) {
    currentScreen = screen;
  }

  function handleBackToDashboard() {
    currentScreen = 'dashboard';
  }

  function handleBackToOnboarding() {
    selectedTrack = null;
    currentScreen = 'onboarding';
  }
</script>

<main class="app-main">
  {#if isLoadingTrack}
    <div class="loading-overlay">
      <div class="spinner"></div>
      <p>Building your curriculum...</p>
    </div>
  {/if}

  {#if currentScreen === 'splash'}
    <Splash onComplete={handleSplashComplete} />
  {:else if currentScreen === 'onboarding'}
    <Onboarding onSelectTrack={handleSelectTrack} />
  {:else if currentScreen === 'dashboard'}
    <Dashboard 
      track={selectedTrack} 
      onNavigate={handleNavigate} 
      onBackToOnboarding={handleBackToOnboarding} 
    />
  {:else if currentScreen === 'vocabulary'}
    <Vocabulary 
      track={selectedTrack} 
      onBack={handleBackToDashboard} 
    />
  {:else if currentScreen === 'chat'}
    <Chat 
      track={selectedTrack} 
      onBack={handleBackToDashboard} 
    />
  {/if}
</main>

<style>
  .app-main {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    width: 100%;
    position: relative;
  }

  .loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(10, 10, 15, 0.85);
    backdrop-filter: blur(10px);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 16px;
    z-index: 9999;
    color: var(--text-secondary);
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.05);
    border-top: 3px solid #6c63ff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
</style>
