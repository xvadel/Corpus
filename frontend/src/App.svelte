<script>
  import Splash from './lib/Splash.svelte';
  import Onboarding from './lib/Onboarding.svelte';
  import Dashboard from './lib/Dashboard.svelte';
  import Vocabulary from './lib/Vocabulary.svelte';
  import Chat from './lib/Chat.svelte';

  let currentScreen = 'splash'; // 'splash' | 'onboarding' | 'dashboard' | 'vocabulary' | 'chat'
  let selectedTrack = null;

  function handleSplashComplete() {
    currentScreen = 'onboarding';
  }

  function handleSelectTrack(track) {
    selectedTrack = track;
    currentScreen = 'dashboard';
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
  }
</style>
