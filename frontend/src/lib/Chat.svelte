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

  // Setup profile based on selected track
  function initializeProfile() {
    if (track.id === 'startup_pitching') {
      botName = 'Alex Mercer';
      botTitle = 'Partner, Apex Ventures';
      botIcon = 'trending_up';
      botGreeting = "Hey there! Thanks for pitching Apex Ventures. Let's talk about your startup. What is your current runway and burn rate?";
      quickReplies = [
        "Our runway is 18 months and burn rate is low.",
        "We have strong traction with 10K active users.",
        "Our valuation is based on early pilot customer revenue.",
      ];
      botResponses = [
        "Interesting. What is your plan to reduce the burn rate? If we invest, how much runway will that give you, and when do you expect to see real traction?",
        "That makes sense. Before we draft a term sheet, we'll need to go through due diligence and check your cap table. What is your valuation expectation?",
        "Understood. Have you ever had to pivot the product, or has the strategy been consistent from day one?",
        "That's a solid point. In a pitch, you really want to highlight your traction and clear financial metrics to give the VC confidence.",
      ];
    } else if (track.id === 'software_engineering') {
      botName = 'Sarah Connor';
      botTitle = 'Principal Tech Architect';
      botIcon = 'developer_mode';
      botGreeting = 'Welcome to the tech design review. We need to scale our notification system. How would you design it to ensure low latency?';
      quickReplies = [
        "We should decouple it with microservices.",
        "Let's put an API Gateway to handle authentication.",
        "I suggest using a load balancer to split traffic.",
      ];
      botResponses = [
        "I see. Moving to microservices can help, but how will you handle the communication between them? Are you putting an API Gateway in front, and how will you configure the load balancer?",
        "Good point. But what about testing? Does your CI/CD pipeline run load tests, and how are you planning to manage the technical debt?",
        "Performance is critical. If our API latency goes up, it will affect the user experience. How do you ensure horizontal scalability?",
        "Agreed. When discussing architecture, always emphasize how scalability and refactoring can mitigate technical debt.",
      ];
    } else {
      botName = 'Michael Vance';
      botTitle = 'Managing Director, Global Tech';
      botIcon = 'badge';
      botGreeting = 'Good morning. We need to review the Q3 product roadmap. Stakeholders are concerned about the churn rate. Any ideas?';
      quickReplies = [
        "Our main KPI is user retention.",
        "Let's align with stakeholders tomorrow.",
        "We need to update our product roadmap.",
      ];
      botResponses = [
        "I see. If we change the strategy, how will that affect our primary KPI? We need a solid ROI to justify this.",
        "Aligning with the stakeholder group is key. What is our go-to-market strategy, and how do we address the customer churn rate?",
        "We have a tight sprint schedule. What is the key deliverable for this cycle, and is it on our product roadmap?",
        "That sounds reasonable. In product management, keeping the roadmap aligned with business KPIs is essential.",
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

  // Helper function to tokenize text and highlight vocab terms
  function tokenizeMessage(text, vocabList) {
    if (!text) return [];
    const lowerText = text.toLowerCase();
    
    // Sort terms by length desc
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

<div class="chat-container" in:fade={{ duration: 300 }}>
  <!-- Top Bar -->
  <div class="chat-header">
    <button class="back-btn" on:click={onBack}>
      <span class="material-icons-round back-icon">arrow_back_ios</span>
    </button>
    
    <!-- Coach Avatar -->
    <div class="avatar-wrapper" style="background: linear-gradient(135deg, {track.accentColor} 0%, #4834df 100%)">
      <span class="material-icons-round avatar-icon">{botIcon === 'trending_up' ? 'trending_up' : botIcon === 'developer_mode' ? 'developer_mode' : 'badge'}</span>
    </div>

    <div class="coach-info">
      <div class="name-row">
        <span class="coach-name">{botName}</span>
        <div class="status-dot"></div>
      </div>
      <span class="coach-title">{botTitle}</span>
    </div>
  </div>

  <!-- Messages List -->
  <div class="chat-messages" bind:this={chatListEl}>
    {#each messages as msg}
      <div class="message-row {msg.isUser ? 'user-row' : 'bot-row'}">
        <div 
          class="message-bubble glass {msg.isUser ? 'user-bubble' : 'bot-bubble'}"
          style="{msg.isUser ? `background: linear-gradient(135deg, ${track.accentColor} 0%, ${track.accentColor}dd 100%); border-color: transparent` : 'border-color: rgba(255, 255, 255, 0.05)'}"
        >
          {#if msg.isUser}
            <p>{msg.text}</p>
          {:else}
            <p>
              {#each tokenizeMessage(msg.text, track.sampleVocabulary) as token}
                {#if token.highlight}
                  <strong class="highlight-vocab" style="color: {track.accentColor}; text-shadow: 0 0 8px {track.accentColor}40">{token.text}</strong>
                {:else}
                  {token.text}
                {/if}
              {/each}
            </p>
          {/if}
        </div>
      </div>
    {/each}

    {#if isTyping}
      <div class="message-row bot-row">
        <div class="message-bubble glass bot-bubble typing-bubble" style="border-color: rgba(255, 255, 255, 0.05)">
          <div class="typing-dot" style="background: {track.accentColor}"></div>
          <div class="typing-dot" style="background: {track.accentColor}; animation-delay: 150ms"></div>
          <div class="typing-dot" style="background: {track.accentColor}; animation-delay: 300ms"></div>
        </div>
      </div>
    {/if}
  </div>

  <!-- Bottom Panel -->
  <div class="chat-bottom-panel">
    <!-- Quick Replies Chips -->
    {#if messages.length > 0 && !messages[messages.length - 1].isUser && !isTyping}
      <div class="quick-replies-row">
        {#each quickReplies as reply}
          <button class="quick-reply-chip glass" on:click={() => handleSend(reply)}>
            {reply}
          </button>
        {/each}
      </div>
    {/if}

    <!-- Input Bar -->
    <form class="input-bar glass" on:submit|preventDefault={() => handleSend(textInput)}>
      <input 
        type="text" 
        bind:value={textInput} 
        placeholder="Type your response..." 
        class="chat-input"
        style="--caret-color: {track.accentColor}"
      />
      <button type="submit" class="send-btn" style="color: {track.accentColor}">
        <span class="material-icons-round">send</span>
      </button>
    </form>
  </div>
</div>

<style>
  .chat-container {
    max-width: 600px;
    width: 100%;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    height: 100vh;
    box-sizing: border-box;
  }

  .chat-header {
    display: flex;
    align-items: center;
    padding: 16px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }

  .back-btn {
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 8px;
    margin-right: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .back-icon {
    font-size: 18px;
    color: white;
  }

  .avatar-wrapper {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
    margin-right: 12px;
  }

  .avatar-icon {
    font-size: 22px;
    color: white;
  }

  .coach-info {
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .name-row {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .coach-name {
    font-size: 15px;
    font-weight: 600;
    color: white;
  }

  .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--success-green);
    box-shadow: 0 0 8px var(--success-green);
    animation: pulse 1.6s infinite alternate;
  }

  .coach-title {
    font-size: 11px;
    color: var(--text-secondary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .chat-messages {
    flex-grow: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .message-row {
    display: flex;
    width: 100%;
  }

  .user-row {
    justify-content: flex-end;
  }

  .bot-row {
    justify-content: flex-start;
  }

  .message-bubble {
    padding: 12px 16px;
    max-width: 75%;
    font-size: 14px;
    line-height: 1.45;
    animation: bubbleUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) both;
  }

  .user-bubble {
    border-radius: 16px 16px 4px 16px;
    color: white;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .bot-bubble {
    border-radius: 16px 16px 16px 4px;
    color: rgba(255, 255, 255, 0.95);
    background: rgba(255, 255, 255, 0.05);
  }

  .highlight-vocab {
    font-weight: 700;
    text-decoration: underline;
  }

  /* Typing animation */
  .typing-bubble {
    display: flex;
    gap: 4px;
    padding: 14px 20px;
    align-items: center;
  }

  .typing-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    opacity: 0.6;
    animation: typingPulse 0.8s infinite alternate;
  }

  /* Input and Quick replies panel */
  .chat-bottom-panel {
    padding: 16px;
  }

  .quick-replies-row {
    display: flex;
    overflow-x: auto;
    gap: 8px;
    padding-bottom: 8px;
    margin-bottom: 12px;
    scrollbar-width: none;
  }

  .quick-replies-row::-webkit-scrollbar {
    display: none;
  }

  .quick-reply-chip {
    flex-shrink: 0;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 6px 14px;
    color: rgba(255, 255, 255, 0.8);
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .quick-reply-chip:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.16);
    color: white;
  }

  .input-bar {
    display: flex;
    align-items: center;
    border-radius: 24px;
    padding: 4px 16px;
    background: rgba(255, 255, 255, 0.04);
    border-color: rgba(255, 255, 255, 0.08);
  }

  .chat-input {
    flex-grow: 1;
    background: transparent;
    border: none;
    outline: none;
    color: white;
    font-size: 14px;
    padding: 8px 0;
    caret-color: var(--caret-color);
  }

  .chat-input::placeholder {
    color: var(--text-muted);
  }

  .send-btn {
    background: transparent;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4px;
  }

  @keyframes pulse {
    from {
      opacity: 0.4;
    }
    to {
      opacity: 1;
    }
  }

  @keyframes bubbleUp {
    0% {
      opacity: 0;
      transform: translateY(8px);
    }
    100% {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes typingPulse {
    0% {
      opacity: 0.2;
      transform: translateY(2px);
    }
    100% {
      opacity: 1;
      transform: translateY(-2px);
    }
  }
</style>
