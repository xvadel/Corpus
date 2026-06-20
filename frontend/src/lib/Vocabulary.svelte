<script>
  import { fade } from 'svelte/transition';

  export let track = null;
  export let onBack = () => {};

  let activeTab = 'flashcards'; // 'flashcards' | 'all'
  let selectedCategory = 'All';
  let currentIndex = 0;
  let isFlipped = false;

  $: vocabulary = track ? track.sampleVocabulary : [];
  $: categories = ['All', ...new Set(vocabulary.map(v => v.category))];
  
  $: filteredTerms = selectedCategory === 'All' 
    ? vocabulary 
    : vocabulary.filter(v => v.category === selectedCategory);

  // Reset indices and flip when category changes
  $: {
    if (selectedCategory) {
      currentIndex = 0;
      isFlipped = false;
    }
  }

  function nextCard() {
    if (currentIndex < filteredTerms.length - 1) {
      isFlipped = false;
      // Wait for flip transition if already flipped, or just change
      setTimeout(() => {
        currentIndex++;
      }, isFlipped ? 150 : 0);
    }
  }

  function prevCard() {
    if (currentIndex > 0) {
      isFlipped = false;
      setTimeout(() => {
        currentIndex--;
      }, isFlipped ? 150 : 0);
    }
  }

  // Accordion active state
  let expandedTermIndex = null;
  function toggleAccordion(index) {
    if (expandedTermIndex === index) {
      expandedTermIndex = null;
    } else {
      expandedTermIndex = index;
    }
  }
</script>

<div class="vocabulary-container" in:fade={{ duration: 300 }}>
  <!-- Header -->
  <div class="header">
    <button class="back-btn" on:click={onBack}>
      <span class="material-icons-round back-icon">arrow_back_ios</span>
    </button>
    <div class="header-text">
      <span class="track-tag" style="color: {track.accentColor}">{track.name}</span>
      <h1 class="page-title">Vocabulary Deck</h1>
    </div>
  </div>

  <!-- Tabs -->
  <div class="tabs-container">
    <button 
      class="tab-btn {activeTab === 'flashcards' ? 'active' : ''}" 
      style="--tab-accent: {track.accentColor}"
      on:click={() => activeTab = 'flashcards'}
    >
      Flashcards
    </button>
    <button 
      class="tab-btn {activeTab === 'all' ? 'active' : ''}" 
      style="--tab-accent: {track.accentColor}"
      on:click={() => activeTab = 'all'}
    >
      All Terms
    </button>
  </div>

  <!-- Categories Chips -->
  <div class="categories-row">
    {#each categories as category}
      <button 
        class="category-chip {selectedCategory === category ? 'active' : ''}"
        style="--chip-accent: {track.accentColor}"
        on:click={() => selectedCategory = category}
      >
        {category}
      </button>
    {/each}
  </div>

  <!-- Content View -->
  {#if filteredTerms.length === 0}
    <div class="empty-state">
      <span class="material-icons-round empty-icon">layers_clear</span>
      <p>No terms found in this category.</p>
    </div>
  {:else}
    <div class="content-view">
      {#if activeTab === 'flashcards'}
        <!-- Flashcard Flip View -->
        <div class="flashcards-wrapper">
          <button class="flashcard-container" on:click={() => isFlipped = !isFlipped}>
            <div class="flashcard-inner {isFlipped ? 'flipped' : ''}">
              
              <!-- Front Side -->
              <div class="card-face card-front glass" style="border-color: rgba(255, 255, 255, 0.08)">
                <span class="card-category" style="background: {track.accentColor}25; color: {track.accentColor}">
                  {filteredTerms[currentIndex].category}
                </span>
                <h2 class="card-term">{filteredTerms[currentIndex].term}</h2>
                <div class="flip-hint">
                  <span class="material-icons-round hint-icon">touch_app</span>
                  <span>Tap to reveal definition</span>
                </div>
              </div>

              <!-- Back Side -->
              <div class="card-face card-back glass" style="border-color: {track.accentColor}40">
                <span class="card-back-label" style="color: {track.accentColor}">Definition</span>
                <p class="card-definition">{filteredTerms[currentIndex].definition}</p>
                
                <div class="card-example-box">
                  <span class="material-icons-round quote-icon" style="color: {track.accentColor}99">format_quote</span>
                  <p class="card-example">{filteredTerms[currentIndex].example}</p>
                </div>
              </div>

            </div>
          </button>

          <!-- Card Controls -->
          <div class="card-controls">
            <button 
              class="control-btn glass {currentIndex === 0 ? 'disabled' : ''}" 
              on:click={prevCard} 
              disabled={currentIndex === 0}
            >
              <span class="material-icons-round">arrow_back</span>
            </button>

            <div class="progress-info">
              <span class="progress-text">Card {currentIndex + 1} of {filteredTerms.length}</span>
              <div class="progress-bar-bg">
                <div 
                  class="progress-bar-fill" 
                  style="width: {((currentIndex + 1) / filteredTerms.length) * 100}%; background: {track.accentColor}"
                ></div>
              </div>
            </div>

            <button 
              class="control-btn glass {currentIndex === filteredTerms.length - 1 ? 'disabled' : ''}" 
              on:click={nextCard} 
              disabled={currentIndex === filteredTerms.length - 1}
            >
              <span class="material-icons-round">arrow_forward</span>
            </button>
          </div>
        </div>

      {:else}
        <!-- All Terms List View -->
        <div class="terms-list">
          {#each filteredTerms as term, index}
            <div class="term-accordion glass">
              <button class="accordion-header" on:click={() => toggleAccordion(index)}>
                <div class="accordion-title-box">
                  <h3 class="accordion-term">{term.term}</h3>
                  <span class="accordion-category" style="color: {track.accentColor}">{term.category}</span>
                </div>
                <span class="material-icons-round accordion-arrow {expandedTermIndex === index ? 'expanded' : ''}">
                  keyboard_arrow_down
                </span>
              </button>
              
              {#if expandedTermIndex === index}
                <div class="accordion-content" in:fade={{ duration: 150 }}>
                  <div class="content-section">
                    <span class="section-label" style="color: {track.accentColor}">Definition:</span>
                    <p class="section-text">{term.definition}</p>
                  </div>
                  <div class="content-section">
                    <span class="section-label" style="color: var(--text-muted)">Example:</span>
                    <p class="section-text example-text">"{term.example.replace(/^["']|["']$/g, '')}"</p>
                  </div>
                </div>
              {/if}
            </div>
          {/each}
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .vocabulary-container {
    max-width: 600px;
    width: 100%;
    margin: 0 auto;
    padding: 24px;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    box-sizing: border-box;
  }

  .header {
    display: flex;
    align-items: center;
    margin-bottom: 24px;
  }

  .back-btn {
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 8px;
    margin-right: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .back-icon {
    font-size: 20px;
    color: white;
  }

  .header-text {
    display: flex;
    flex-direction: column;
  }

  .track-tag {
    font-size: 12px;
    font-weight: 500;
  }

  .page-title {
    font-size: 24px;
    font-weight: 600;
  }

  .tabs-container {
    display: flex;
    height: 48px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 4px;
    margin-bottom: 20px;
  }

  .tab-btn {
    flex: 1;
    border: none;
    border-radius: 10px;
    background: transparent;
    color: var(--text-secondary);
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.25s ease;
  }

  .tab-btn.active {
    background: var(--tab-accent);
    color: white;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
  }

  .categories-row {
    display: flex;
    overflow-x: auto;
    gap: 8px;
    padding-bottom: 8px;
    margin-bottom: 24px;
    scrollbar-width: none; /* Firefox */
  }

  .categories-row::-webkit-scrollbar {
    display: none; /* Safari/Chrome */
  }

  .category-chip {
    flex-shrink: 0;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 6px 16px;
    color: var(--text-secondary);
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .category-chip.active {
    background: var(--chip-accent);
    color: white;
    border-color: transparent;
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px;
    text-align: center;
    color: var(--text-secondary);
  }

  .empty-icon {
    font-size: 64px;
    color: var(--text-muted);
    margin-bottom: 16px;
  }

  .content-view {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
  }

  /* Flashcards Styling */
  .flashcards-wrapper {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    justify-content: space-between;
  }

  .flashcard-container {
    width: 100%;
    height: 320px;
    background: transparent;
    border: none;
    padding: 0;
    perspective: 1000px;
    cursor: pointer;
    outline: none;
    text-align: left;
    margin-bottom: 32px;
  }

  .flashcard-inner {
    position: relative;
    width: 100%;
    height: 100%;
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    transform-style: preserve-3d;
  }

  .flashcard-inner.flipped {
    transform: rotateY(180deg);
  }

  .card-face {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    border-radius: 24px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-sizing: border-box;
  }

  .card-front {
    background: rgba(255, 255, 255, 0.04);
    align-items: flex-start;
  }

  .card-category {
    font-size: 11px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 8px;
    margin-bottom: 18px;
  }

  .card-term {
    font-size: 28px;
    font-weight: 700;
    color: white;
    margin-bottom: 16px;
  }

  .flip-hint {
    display: flex;
    align-items: center;
    color: var(--text-muted);
    font-size: 12px;
    font-style: italic;
    gap: 6px;
  }

  .hint-icon {
    font-size: 16px;
  }

  .card-back {
    background: rgba(255, 255, 255, 0.08);
    transform: rotateY(180deg);
    align-items: flex-start;
  }

  .card-back-label {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
  }

  .card-definition {
    font-size: 15px;
    line-height: 1.6;
    color: rgba(255, 255, 255, 0.95);
    margin-bottom: 20px;
  }

  .card-example-box {
    width: 100%;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 14px;
    padding: 14px;
    display: flex;
    gap: 8px;
    box-sizing: border-box;
  }

  .quote-icon {
    font-size: 20px;
    margin-top: -4px;
  }

  .card-example {
    font-size: 13px;
    line-height: 1.5;
    font-style: italic;
    color: rgba(255, 255, 255, 0.7);
  }

  /* Card Controls Styling */
  .card-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 10px;
  }

  .control-btn {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.05);
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .control-btn:not(.disabled):hover {
    background: rgba(255, 255, 255, 0.12);
    transform: scale(1.05);
  }

  .control-btn.disabled {
    opacity: 0.2;
    cursor: not-allowed;
  }

  .progress-info {
    flex-grow: 1;
    margin: 0 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .progress-text {
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 8px;
  }

  .progress-bar-bg {
    width: 100%;
    max-width: 160px;
    height: 4px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
    overflow: hidden;
  }

  .progress-bar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.3s ease;
  }

  /* Terms List Styling */
  .terms-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding-bottom: 24px;
  }

  .term-accordion {
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    background: rgba(255, 255, 255, 0.03);
    overflow: hidden;
    transition: all 0.3s ease;
  }

  .accordion-header {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    background: transparent;
    border: none;
    text-align: left;
    cursor: pointer;
  }

  .accordion-title-box {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .accordion-term {
    font-size: 16px;
    font-weight: 600;
    color: white;
  }

  .accordion-category {
    font-size: 11px;
    font-weight: 500;
  }

  .accordion-arrow {
    font-size: 24px;
    color: var(--text-secondary);
    transition: transform 0.3s ease;
  }

  .accordion-arrow.expanded {
    transform: rotate(180deg);
  }

  .accordion-content {
    padding: 0 20px 20px 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.03);
  }

  .content-section {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .section-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
  }

  .section-text {
    font-size: 13px;
    line-height: 1.5;
    color: rgba(255, 255, 255, 0.9);
  }

  .example-text {
    font-style: italic;
    color: rgba(255, 255, 255, 0.65);
  }
</style>
