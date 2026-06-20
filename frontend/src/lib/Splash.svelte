<script>
  import { onMount } from 'svelte';

  export let onComplete = () => {};

  onMount(() => {
    const timer = setTimeout(() => {
      onComplete();
    }, 2800);

    return () => clearTimeout(timer);
  });
</script>

<div class="splash-container">
  <div class="logo-box">
    <span class="material-icons-round logo-icon">translate</span>
  </div>
  <h1 class="title">Corpus</h1>
  <p class="tagline">Speak your industry's language</p>
  
  <div class="loader">
    <div class="spinner"></div>
  </div>
</div>

<style>
  .splash-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    width: 100%;
    position: relative;
    padding: 20px;
    box-sizing: border-box;
  }

  .logo-box {
    width: 100px;
    height: 100px;
    background: linear-gradient(135deg, #6c63ff 0%, #4834df 100%);
    border-radius: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 12px 40px rgba(108, 99, 255, 0.4);
    animation: bounceIn 1.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  }

  .logo-icon {
    font-size: 48px;
    color: white;
  }

  .title {
    font-size: 42px;
    margin-top: 32px;
    margin-bottom: 12px;
    letter-spacing: 2px;
    font-weight: 700;
    opacity: 0;
    animation: fadeInUp 0.8s ease-out 0.3s forwards;
  }

  .tagline {
    font-size: 16px;
    color: var(--text-muted);
    letter-spacing: 0.5px;
    margin-bottom: 60px;
    opacity: 0;
    animation: fadeIn 0.8s ease-out 0.6s forwards;
  }

  .loader {
    width: 28px;
    height: 28px;
    opacity: 0;
    animation: fadeIn 0.6s ease-out 0.9s forwards;
  }

  .spinner {
    width: 100%;
    height: 100%;
    border: 2.5px solid rgba(108, 99, 255, 0.15);
    border-top: 2.5px solid rgba(108, 99, 255, 0.6);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes bounceIn {
    0% {
      opacity: 0;
      transform: scale(0.5);
    }
    100% {
      opacity: 1;
      transform: scale(1);
    }
  }

  @keyframes fadeInUp {
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
    0% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
</style>
