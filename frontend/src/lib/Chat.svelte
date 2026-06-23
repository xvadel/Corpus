<script>
  import { onMount, tick } from 'svelte';
  import { fade } from 'svelte/transition';

  export let track = null;
  export let onBack = () => {};

  let messages = [];
  let textInput = '';
  let isTyping = false;
  let botResponseIndex = 0;
  let chatListEl = null;

  // Bot Profiles based on track
  let botName = '';
  let botTitle = '';
  let botIcon = '';
  let botGreeting = '';
  let quickReplies = [];
  let botResponses = [];
  
  // Evaluation Stats (Interactive mock telemetry)
  let techAccuracy = 85;
  let professionalism = 90;
  let marketAlignment = 60;
  let skepticismLevel = 'ELEVATED - PRESSURE ON';
  let skepticismDot = '#F59E0B'; // Orange
  let internalThoughts = "The candidate seems capable, but I need to test if they understand how their system scales under pressure.";

  function initializeProfile() {
    if (track.id === 'startup_pitching' || track.id === 'ai_engineering') {
      botName = track.id === 'ai_engineering' ? 'Dr. Evelyn Vance' : 'Alex Mercer';
      botTitle = track.id === 'ai_engineering' ? 'Lead AI Architect' : 'Partner, Apex Ventures';
      botIcon = 'trending_up';
      botGreeting = track.id === 'ai_engineering' 
        ? "Hello! Let's review the AI system architecture. How are you handling vector storage and context injection limits?"
        : "Hey there! Thanks for pitching Apex Ventures. Let's talk about your startup. What is your current runway and burn rate?";
      quickReplies = track.id === 'ai_engineering'
        ? [
            "We use hybrid quantization decoupled from topological index.",
            "We use chunking with metadata extraction and ChromaDB.",
            "We are validating retrieval faithfulness via RAGAS metrics."
          ]
        : [
            "Our runway is 18 months and burn rate is low.",
            "We have strong traction with 10K active users.",
            "Our valuation is based on early pilot customer revenue."
          ];
      botResponses = track.id === 'ai_engineering'
        ? [
            "Decoupling the index helps with scalability, but what about latency? How do you maintain search accuracy beyond 10PB?",
            "That works for search, but how are you mitigating latency spikes during Cross-Encoder reranking?",
            "RAGAS evaluates faithfulness well, but does it cover multi-step agent planning limits?",
            "Excellent. A systematic approach to semantic indexing is the only way to minimize context constraints."
          ]
        : [
            "Interesting. What's your plan to reduce burn rate? With our investment, what runway does that give you?",
            "Before a term sheet, we'll need due diligence — walk me through your cap table and current valuation.",
            "Your traction numbers look promising. Have you had to pivot the product since day one?",
            "Solid pitch. Focus on measurable traction and clean financial metrics to give VCs real confidence."
          ];
    } else if (track.id === 'software_engineering') {
      botName = 'Sarah Connor';
      botTitle = 'Principal Tech Architect';
      botIcon = 'developer_mode';
      botGreeting = 'Welcome to the tech design review. We need to scale our notification system. How would you design it to ensure low latency?';
      quickReplies = [
        "We should decouple it with microservices.",
        "Let's put an API Gateway to handle authentication.",
        "I suggest using a load balancer to split traffic."
      ];
      botResponses = [
        "I see. Moving to microservices can help, but how will you handle the communication between them? Are you putting an API Gateway in front, and how will you configure the load balancer?",
        "Good point. But what about testing? Does your CI/CD pipeline run load tests, and how are you planning to manage the technical debt?",
        "Performance is critical. If our API latency goes up, it will affect the user experience. How do you ensure horizontal scalability?",
        "Agreed. When discussing architecture, always emphasize how scalability and refactoring can mitigate technical debt."
      ];
    } else {
      botName = 'Michael Vance';
      botTitle = 'Managing Director, Global Tech';
      botIcon = 'badge';
      botGreeting = 'Good morning. We need to review the Q3 product roadmap. Stakeholders are concerned about the churn rate. Any ideas?';
      quickReplies = [
        "Our main KPI is user retention.",
        "Let's align with stakeholders tomorrow.",
        "We need to update our product roadmap."
      ];
      botResponses = [
        "I see. If we change the strategy, how will that affect our primary KPI? We need a solid ROI to justify this.",
        "Aligning with the stakeholder group is key. What is our go-to-market strategy, and how do we address the customer churn rate?",
        "We have a tight sprint schedule. What is the key deliverable for this cycle, and is it on our product roadmap?",
        "That sounds reasonable. In product management, keeping the roadmap aligned with business KPIs is essential."
      ];
    }

    messages = [
      {
        text: botGreeting,
        isUser: false,
        timestamp: new Date()
      }
    ];
  }

  onMount(() => {
    initializeProfile();
    scrollToBottom();
  });

  async function scrollToBottom() {
    await tick();
    if (chatListEl) {
      chatListEl.scrollTop = chatListEl.scrollHeight;
    }
  }

  function updateMockTelemetry(userMsg) {
    // Dynamic updates based on vocabulary keywords in the user's message
    const msgLower = userMsg.toLowerCase();
    
    // Check if user is using good tech terms
    if (msgLower.includes('quantization') || msgLower.includes('decouple') || msgLower.includes('chunking') || msgLower.includes('ragas') || msgLower.includes('runway') || msgLower.includes('traction') || msgLower.includes('microservices')) {
      techAccuracy = Math.min(100, techAccuracy + Math.floor(Math.random() * 5) + 3);
      professionalism = Math.min(100, professionalism + Math.floor(Math.random() * 3) + 2);
      marketAlignment = Math.min(100, marketAlignment + Math.floor(Math.random() * 6) + 4);
      skepticismLevel = 'REDUCING - IMPRESSED';
      skepticismDot = '#10B981'; // Green
      internalThoughts = "Good usage of structural terminology. The speaker understands the technical trade-offs of their design choices.";
    } else {
      techAccuracy = Math.max(50, techAccuracy - Math.floor(Math.random() * 4));
      skepticismLevel = 'ELEVATED - PRESSURE ON';
      skepticismDot = '#EF4444'; // Red
      internalThoughts = "The candidate is giving generic answers. I will press them for direct metrics and low-level details.";
    }
  }

  function handleSend(text) {
    if (!text.trim()) return;

    // Add user message
    messages = [...messages, {
      text: text,
      isUser: true,
      timestamp: new Date()
    }];
    textInput = '';
    scrollToBottom();

    // Update evaluation metrics dynamically based on inputs
    updateMockTelemetry(text);

    // Trigger typing response
    isTyping = true;
    scrollToBottom();

    setTimeout(async () => {
      try {
        const res = await fetch('/api/chat/message', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            track_id: track.id,
            user_message: text,
            history_length: messages.length
          })
        });
        
        if (!res.ok) throw new Error('API request failed');
        const data = await res.json();
        
        isTyping = false;
        messages = [...messages, {
          text: data.reply,
          isUser: false,
          timestamp: new Date()
        }];
      } catch (err) {
        console.error("Chat API failed, falling back to local simulation:", err);
        isTyping = false;
        const botReply = botResponses[botResponseIndex % botResponses.length];
        botResponseIndex++;

        messages = [...messages, {
          text: botReply,
          isUser: false,
          timestamp: new Date()
        }];
      }
      scrollToBottom();
    }, 1200);
  }

  function tokenizeMessage(text, vocabList) {
    if (!text) return [];
    const lowerText = text.toLowerCase();
    const sortedVocab = [...vocabList].sort((a, b) => b.term.length - a.term.length);
    
    let matches = [];
    for (let vocab of sortedVocab) {
      const term = vocab.term.toLowerCase();
      let index = 0;
      while (true) {
        index = lowerText.indexOf(term, index);
        if (index === -1) break;
        
        const overlaps = matches.some(m => index < m.end && index + term.length > m.start);
        if (!overlaps) {
          matches.push({
            start: index,
            end: index + term.length,
            term: vocab.term
          });
        }
        index += term.length;
      }
    }
    
    matches.sort((a, b) => a.start - b.start);
    
    let tokens = [];
    let currentPos = 0;
    for (let match of matches) {
      if (match.start > currentPos) {
        tokens.push({
          text: text.substring(currentPos, match.start),
          highlight: false
        });
      }
      tokens.push({
        text: text.substring(match.start, match.end),
        highlight: true
      });
      currentPos = match.end;
    }
    
    if (currentPos < text.length) {
      tokens.push({
        text: text.substring(currentPos),
        highlight: false
      });
    }
    
    return tokens;
  }
</script>

<div class="simulator-layout" in:fade={{ duration: 250 }}>
  <!-- 1. LEFT SIDEBAR: Navigation Panel -->
  <aside class="sidebar">
    <div class="sidebar-top">
      <div class="sidebar-logo">
        <img src="/corpus_icon.svg" alt="Corpus Icon" class="icon-img" />
        <div class="logo-text">
          <span class="logo-name">Corpus AI</span>
          <span class="logo-tagline">Precision Minimalism</span>
        </div>
      </div>
      
      <nav class="nav-menu">
        <button class="nav-item" on:click={onBack}>
          <span class="material-icons-round">home</span> Home
        </button>
        <button class="nav-item disabled">
          <span class="material-icons-round">folder</span> Projects
        </button>
        <button class="nav-item" on:click={onBack}>
          <span class="material-icons-round">school</span> Learning
        </button>
        <button class="nav-item active">
          <span class="material-icons-round">terminal</span> Simulator
        </button>
        <button class="nav-item disabled">
          <span class="material-icons-round">psychology</span> Intelligence
        </button>
      </nav>
    </div>

    <div class="sidebar-bottom">
      <button class="analyze-btn" on:click={onBack}>Back to Dashboard</button>
      <div class="bottom-links">
        <span class="b-link">Settings</span>
        <span class="b-link">Support</span>
      </div>
    </div>
  </aside>

  <!-- 2. CENTER PANEL: Investor Simulator Chat Room -->
  <main class="chat-main">
    <!-- Header -->
    <header class="chat-header">
      <div class="header-left">
        <h2>Investor Simulator</h2>
        <span class="session-badge"><span class="green-dot"></span> Session Active</span>
        <span class="phase-badge">• Series A Round</span>
      </div>
      <div class="header-right">
        <span class="material-icons-round h-icon">notifications</span>
        <div class="avatar">
          <img src="https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=100&q=80" alt="Avatar" />
        </div>
      </div>
    </header>

    <!-- Chat Area -->
    <div class="chat-area" bind:this={chatListEl}>
      <div class="interaction-banner">
        <h3>Investor Interaction</h3>
        <span class="engine-badge">Real-time LLM Synthesis Engine</span>
      </div>

      {#each messages as msg}
        <div class="msg-block {msg.isUser ? 'founder-block' : 'coach-block'}">
          <div class="msg-avatar">
            <span class="material-icons-round">
              {msg.isUser ? 'person' : 'insights'}
            </span>
          </div>
          <div class="msg-bubble-container">
            <span class="bubble-sender">{msg.isUser ? 'FOUNDER (YOU)' : botName.toUpperCase()}</span>
            <div class="msg-bubble">
              {#if msg.isUser}
                <p>{msg.text}</p>
              {:else}
                <p>
                  {#each tokenizeMessage(msg.text, track.sampleVocabulary) as token}
                    {#if token.highlight}
                      <span class="vocab-highlight">{token.text}</span>
                    {:else}
                      {token.text}
                    {/if}
                  {/each}
                </p>
              {/if}
            </div>
            
            {#if !msg.isUser}
              <div class="tag-chips">
                <span class="tag-chip danger">HIGH STAKES QUESTION</span>
                <span class="tag-chip info">TECHNICAL DEPTH: 9/10</span>
              </div>
            {/if}
          </div>
        </div>
      {/each}

      {#if isTyping}
        <div class="msg-block coach-block">
          <div class="msg-avatar">
            <span class="material-icons-round">insights</span>
          </div>
          <div class="msg-bubble-container">
            <span class="bubble-sender">{botName.toUpperCase()}</span>
            <div class="msg-bubble typing-indicator">
              <span class="dot"></span>
              <span class="dot"></span>
              <span class="dot"></span>
            </div>
          </div>
        </div>
      {/if}
    </div>

    <!-- Input Box -->
    <div class="input-panel">
      <!-- Quick replies chips -->
      {#if messages.length > 0 && !messages[messages.length - 1].isUser && !isTyping}
        <div class="replies-row">
          {#each quickReplies as reply}
            <button class="reply-chip" on:click={() => handleSend(reply)}>
              {reply}
            </button>
          {/each}
        </div>
      {/if}

      <form class="input-form" on:submit|preventDefault={() => handleSend(textInput)}>
        <input 
          type="text" 
          bind:value={textInput} 
          placeholder="Formulate your strategic response..." 
          class="strategic-input" 
        />
        <button class="send-arrow-btn" type="submit">
          <span class="material-icons-round">arrow_upward</span>
        </button>
      </form>

      <div class="input-actions">
        <span class="i-action"><span class="material-icons-round">attach_file</span> ATTACH DECK</span>
        <span class="i-action"><span class="material-icons-round">analytics</span> TECHNICAL APPENDICES</span>
        <span class="i-action-hint">PRESS ENTER TO COMMIT RESPONSE</span>
      </div>
    </div>
  </main>

  <!-- 3. RIGHT SIDEBAR: Pitch Evaluations -->
  <aside class="eval-panel">
    <div class="eval-section">
      <h3 class="panel-section-title">PITCH EVALUATION</h3>
      
      <!-- Metric Item 1 -->
      <div class="eval-card">
        <div class="eval-card-header">
          <span>Technical Accuracy</span>
          <span class="eval-score text-green">{techAccuracy}%</span>
        </div>
        <div class="gauge-bar">
          <div class="gauge-fill bg-green" style="width: {techAccuracy}%"></div>
        </div>
        <p class="eval-feedback">
          {techAccuracy >= 85 
            ? "Superior grasp of vector mechanics. Explanations of indexing are sound, showing high readiness for technical DD."
            : "Explanation lacks low-level details. Try using specific terminology like embeddings, quantization, or RAG architectures."}
        </p>
      </div>

      <!-- Metric Item 2 -->
      <div class="eval-card">
        <div class="eval-card-header">
          <span>Professionalism</span>
          <span class="eval-score text-blue">{professionalism}%</span>
        </div>
        <div class="gauge-bar">
          <div class="gauge-fill bg-blue" style="width: {professionalism}%"></div>
        </div>
        <p class="eval-feedback">
          Tone is confident, measured, and structured. Your speed metrics represent high cognitive preparedness.
        </p>
      </div>

      <!-- Metric Item 3 -->
      <div class="eval-card">
        <div class="eval-card-header">
          <span>Market Alignment</span>
          <span class="eval-score text-grey">{marketAlignment}%</span>
        </div>
        <div class="gauge-bar">
          <div class="gauge-fill bg-grey" style="width: {marketAlignment}%"></div>
        </div>
        <p class="eval-feedback">
          Economic feasibility is still being stress-tested. The VC is analyzing product roadmap metrics and scalability.
        </p>
      </div>
    </div>

    <!-- Investor Internal State Card -->
    <div class="state-section">
      <h3 class="panel-section-title">INVESTOR INTERNAL STATE</h3>
      <div class="state-card">
        <div class="state-card-header">
          <span class="material-icons-round">show_chart</span>
          <div>
            <span class="state-label">Skepticism Level</span>
            <span class="state-val" style="color: {skepticismDot}">{skepticismLevel}</span>
          </div>
          <span class="status-dot-indicator" style="background-color: {skepticismDot}"></span>
        </div>
        
        <p class="quote-block">
          "{internalThoughts}"
        </p>
      </div>
    </div>

    <!-- Request Term Sheet CTA -->
    <div class="cta-wrapper">
      <button class="term-sheet-btn" on:click={() => alert('Term Sheet Request Submitted! Checking evaluation scores...')} disabled={techAccuracy < 80}>
        <span class="material-icons-round">description</span> REQUEST TERM SHEET
      </button>
    </div>
  </aside>
</div>

<style>
  .simulator-layout {
    display: grid;
    grid-template-columns: 240px 1fr 340px;
    height: 100vh;
    width: 100%;
    background-color: var(--bg-dark-content); /* Theme Dark Background */
    color: var(--text-dark-primary);
    overflow: hidden;
  }

  /* 1. LEFT SIDEBAR */
  .sidebar {
    background-color: var(--bg-dark-sidebar);
    border-right: 1px solid var(--border-dark);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 24px 16px;
    height: 100%;
  }

  .sidebar-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 32px;
  }

  .icon-img {
    width: 32px;
    height: 32px;
  }

  .logo-text {
    display: flex;
    flex-direction: column;
  }

  .logo-name {
    font-size: 15px;
    font-weight: 700;
    color: white;
  }

  .logo-tagline {
    font-size: 10px;
    color: var(--text-dark-muted);
    font-weight: 500;
  }

  .nav-menu {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    width: 100%;
    background: none;
    border: none;
    padding: 10px 12px;
    border-radius: 8px;
    color: var(--text-dark-secondary);
    font-size: 13.5px;
    font-weight: 600;
    cursor: pointer;
    text-align: left;
    transition: background-color 0.2s, color 0.2s;
  }

  .nav-item span {
    font-size: 18px;
  }

  .nav-item:hover:not(.disabled) {
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
  }

  .nav-item.active {
    background-color: rgba(255, 255, 255, 0.08);
    color: white;
  }

  .nav-item.disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }

  .sidebar-bottom {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .analyze-btn {
    background-color: white;
    color: #0F172A;
    border: none;
    padding: 10px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 13px;
    cursor: pointer;
    text-align: center;
    transition: background-color 0.2s;
  }

  .analyze-btn:hover {
    background-color: #E2E8F0;
  }

  .bottom-links {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: var(--text-dark-muted);
    font-weight: 600;
  }

  .b-link {
    cursor: pointer;
  }

  .b-link:hover {
    color: var(--text-dark-secondary);
  }

  /* 2. CENTER PANEL */
  .chat-main {
    display: flex;
    flex-direction: column;
    height: 100%;
    border-right: 1px solid var(--border-dark);
  }

  .chat-header {
    height: 70px;
    border-bottom: 1px solid var(--border-dark);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 24px;
    background-color: rgba(26, 29, 36, 0.8);
    backdrop-filter: blur(10px);
  }

  .header-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .header-left h2 {
    font-size: 18px;
    font-weight: 700;
    color: white;
  }

  .session-badge {
    font-size: 11px;
    font-weight: 600;
    color: #10B981;
    background-color: rgba(16, 185, 129, 0.1);
    padding: 3px 8px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .green-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: #10B981;
    box-shadow: 0 0 6px #10B981;
  }

  .phase-badge {
    font-size: 11.5px;
    color: var(--text-dark-muted);
    font-weight: 500;
  }

  .header-right {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .h-icon {
    font-size: 20px;
    color: var(--text-dark-secondary);
    cursor: pointer;
  }

  .avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    overflow: hidden;
    border: 1px solid var(--border-dark);
  }

  .avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  /* Chat Area */
  .chat-area {
    flex-grow: 1;
    overflow-y: auto;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .interaction-banner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border-dark);
    margin-bottom: 8px;
  }

  .interaction-banner h3 {
    font-size: 13px;
    font-weight: 700;
    color: white;
    letter-spacing: 0.5px;
  }

  .engine-badge {
    font-size: 10.5px;
    font-weight: 600;
    color: var(--text-dark-muted);
  }

  .msg-block {
    display: flex;
    gap: 16px;
    max-width: 85%;
  }

  .founder-block {
    align-self: flex-end;
    flex-direction: row-reverse;
    text-align: right;
  }

  .coach-block {
    align-self: flex-start;
  }

  .msg-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background-color: #2D3139;
    border: 1px solid var(--border-dark);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .msg-avatar span {
    font-size: 18px;
    color: var(--text-dark-secondary);
  }

  .founder-block .msg-avatar {
    background-color: white;
  }

  .founder-block .msg-avatar span {
    color: #0F172A;
  }

  .msg-bubble-container {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .bubble-sender {
    font-size: 9.5px;
    font-weight: 700;
    color: var(--text-dark-muted);
    letter-spacing: 0.8px;
  }

  .msg-bubble {
    background-color: #20242D;
    border: 1px solid var(--border-dark);
    border-radius: 12px;
    padding: 16px;
    color: rgba(255, 255, 255, 0.95);
    font-size: 13.5px;
    line-height: 1.5;
    text-align: left;
  }

  .founder-block .msg-bubble {
    background-color: #FFFFFF;
    color: #0F172A;
    border-color: transparent;
  }

  .vocab-highlight {
    font-weight: 700;
    color: #38BDF8;
    background-color: rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.2);
    padding: 1px 4px;
    border-radius: 4px;
  }

  .tag-chips {
    display: flex;
    gap: 8px;
    margin-top: 4px;
  }

  .tag-chip {
    font-size: 9.5px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    letter-spacing: 0.5px;
  }

  .tag-chip.danger {
    color: #F87171;
    background-color: rgba(248, 113, 113, 0.1);
  }

  .tag-chip.info {
    color: #38BDF8;
    background-color: rgba(56, 189, 248, 0.1);
  }

  /* Typing Dot Animation */
  .typing-indicator {
    display: flex;
    gap: 4px;
    padding: 14px 20px;
  }

  .typing-indicator .dot {
    width: 6px;
    height: 6px;
    background-color: var(--text-dark-secondary);
    border-radius: 50%;
    animation: typing 1s infinite alternate;
  }

  .typing-indicator .dot:nth-child(2) { animation-delay: 150ms; }
  .typing-indicator .dot:nth-child(3) { animation-delay: 300ms; }

  @keyframes typing {
    from { opacity: 0.3; transform: translateY(2px); }
    to { opacity: 1; transform: translateY(-2px); }
  }

  /* Input Panel */
  .input-panel {
    border-top: 1px solid var(--border-dark);
    padding: 20px 24px;
    background-color: #16191E;
  }

  .replies-row {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding-bottom: 12px;
    scrollbar-width: none;
  }

  .replies-row::-webkit-scrollbar {
    display: none;
  }

  .reply-chip {
    flex-shrink: 0;
    background-color: #20242C;
    border: 1px solid var(--border-dark);
    color: var(--text-dark-secondary);
    font-size: 11.5px;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 16px;
    cursor: pointer;
    transition: background-color 0.2s, color 0.2s;
  }

  .reply-chip:hover {
    background-color: #2D323F;
    color: white;
  }

  .input-form {
    display: flex;
    align-items: center;
    background-color: #20242D;
    border: 1px solid var(--border-dark);
    border-radius: 12px;
    padding: 4px 8px;
    margin-bottom: 12px;
  }

  .strategic-input {
    flex-grow: 1;
    background: transparent;
    border: none;
    outline: none;
    color: white;
    font-size: 13.5px;
    padding: 10px 8px;
  }

  .strategic-input::placeholder {
    color: var(--text-dark-muted);
  }

  .send-arrow-btn {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background-color: white;
    color: #0F172A;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .send-arrow-btn:hover {
    background-color: #E2E8F0;
  }

  .send-arrow-btn span {
    font-size: 18px;
  }

  .input-actions {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .i-action {
    font-size: 11px;
    font-weight: 700;
    color: var(--text-dark-secondary);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .i-action span {
    font-size: 14px;
  }

  .i-action:hover {
    color: white;
  }

  .i-action-hint {
    font-size: 10.5px;
    font-weight: 500;
    color: var(--text-dark-muted);
    margin-left: auto;
  }

  /* 3. RIGHT PANEL */
  .eval-panel {
    background-color: var(--bg-dark-sidebar);
    padding: 24px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    overflow-y: auto;
  }

  .panel-section-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    color: var(--text-dark-muted);
    margin-bottom: 20px;
  }

  .eval-card {
    background-color: #1A1D24;
    border: 1px solid var(--border-dark);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
  }

  .eval-card-header {
    display: flex;
    justify-content: space-between;
    font-size: 12.5px;
    font-weight: 600;
    color: var(--text-dark-secondary);
    margin-bottom: 8px;
  }

  .eval-score {
    font-weight: 700;
  }

  .text-green { color: #10B981; }
  .text-blue { color: #3B82F6; }
  .text-grey { color: #9CA3AF; }

  .gauge-bar {
    height: 4px;
    background-color: #2D3139;
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 12px;
  }

  .gauge-fill {
    height: 100%;
    border-radius: 2px;
  }

  .gauge-fill.bg-green { background-color: #10B981; }
  .gauge-fill.bg-blue { background-color: #3B82F6; }
  .gauge-fill.bg-grey { background-color: #6B7280; }

  .eval-feedback {
    font-size: 11px;
    line-height: 1.45;
    color: var(--text-dark-muted);
  }

  /* State Card Section */
  .state-section {
    margin-top: 16px;
  }

  .state-card {
    background-color: #1A1D24;
    border: 1px solid var(--border-dark);
    border-radius: 12px;
    padding: 16px;
  }

  .state-card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
    position: relative;
  }

  .state-card-header span:first-child {
    font-size: 18px;
    color: var(--text-dark-muted);
  }

  .state-label {
    display: block;
    font-size: 9.5px;
    font-weight: 700;
    color: var(--text-dark-muted);
    letter-spacing: 0.5px;
  }

  .state-val {
    font-size: 12px;
    font-weight: 700;
  }

  .status-dot-indicator {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    position: absolute;
    top: 4px;
    right: 0;
  }

  .quote-block {
    font-size: 11.5px;
    line-height: 1.5;
    font-style: italic;
    color: #9CA3AF;
    background-color: rgba(255, 255, 255, 0.02);
    border-left: 2px solid var(--border-dark);
    padding-left: 10px;
    margin: 0;
  }

  /* CTA Button */
  .cta-wrapper {
    margin-top: 32px;
  }

  .term-sheet-btn {
    width: 100%;
    background-color: #DC2626; /* Crimson Red button like reference UI */
    color: white;
    border: none;
    border-radius: 8px;
    padding: 14px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.8px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .term-sheet-btn:hover:not(:disabled) {
    background-color: #B91C1C;
  }

  .term-sheet-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .term-sheet-btn span {
    font-size: 16px;
  }
</style>
