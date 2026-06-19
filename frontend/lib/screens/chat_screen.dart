import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../theme/app_theme.dart';
import '../models/track.dart';

class ChatMessage {
  final String text;
  final bool isUser;
  final DateTime timestamp;

  ChatMessage({
    required this.text,
    required this.isUser,
    required this.timestamp,
  });
}

class ChatScreen extends StatefulWidget {
  final Track track;

  const ChatScreen({super.key, required this.track});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final List<ChatMessage> _messages = [];
  final TextEditingController _textController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  bool _isTyping = false;
  int _botResponseIndex = 0;

  // Bot profiles based on track
  late String _botName;
  late String _botTitle;
  late IconData _botIcon;
  late String _botGreeting;
  late List<String> _quickReplies;
  late List<String> _botResponses;

  @override
  void initState() {
    super.initState();
    _initializeChatProfile();
  }

  @override
  void dispose() {
    _textController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _initializeChatProfile() {
    if (widget.track.id == 'startup_pitching') {
      _botName = 'Alex Mercer';
      _botTitle = 'Partner, Apex Ventures';
      _botIcon = Icons.trending_up_rounded;
      _botGreeting = "Hey there! Thanks for pitching Apex Ventures. Let's talk about your startup. What is your current runway and burn rate?";
      _quickReplies = [
        "Our runway is 18 months and burn rate is low.",
        "We have strong traction with 10K active users.",
        "Our valuation is based on early pilot customer revenue.",
      ];
      _botResponses = [
        "Interesting. What is your plan to reduce the burn rate? If we invest, how much runway will that give you, and when do you expect to see real traction?",
        "That makes sense. Before we draft a term sheet, we'll need to go through due diligence and check your cap table. What is your valuation expectation?",
        "Understood. Have you ever had to pivot the product, or has the strategy been consistent from day one?",
        "That's a solid point. In a pitch, you really want to highlight your traction and clear financial metrics to give the VC confidence.",
      ];
    } else if (widget.track.id == 'software_engineering') {
      _botName = 'Sarah Connor';
      _botTitle = 'Principal Tech Architect';
      _botIcon = Icons.developer_mode_rounded;
      _botGreeting = 'Welcome to the tech design review. We need to scale our notification system. How would you design it to ensure low latency?';
      _quickReplies = [
        "We should decouple it with microservices.",
        "Let's put an API Gateway to handle authentication.",
        "I suggest using a load balancer to split traffic.",
      ];
      _botResponses = [
        "I see. Moving to microservices can help, but how will you handle the communication between them? Are you putting an API Gateway in front, and how will you configure the load balancer?",
        "Good point. But what about testing? Does your CI/CD pipeline run load tests, and how are you planning to manage the technical debt?",
        "Performance is critical. If our API latency goes up, it will affect the user experience. How do you ensure horizontal scalability?",
        "Agreed. When discussing architecture, always emphasize how scalability and refactoring can mitigate technical debt.",
      ];
    } else {
      _botName = 'Michael Vance';
      _botTitle = 'Managing Director, Global Tech';
      _botIcon = Icons.badge_rounded;
      _botGreeting = 'Good morning. We need to review the Q3 product roadmap. Stakeholders are concerned about the churn rate. Any ideas?';
      _quickReplies = [
        "Our main KPI is user retention.",
        "Let's align with stakeholders tomorrow.",
        "We need to update our product roadmap.",
      ];
      _botResponses = [
        "I see. If we change the strategy, how will that affect our primary KPI? We need a solid ROI to justify this.",
        "Aligning with the stakeholder group is key. What is our go-to-market strategy, and how do do we address the customer churn rate?",
        "We have a tight sprint schedule. What is the key deliverable for this cycle, and is it on our product roadmap?",
        "That sounds reasonable. In product management, keeping the roadmap aligned with business KPIs is essential.",
      ];
    }

    // Add initial greeting message
    _messages.add(ChatMessage(
      text: _botGreeting,
      isUser: false,
      timestamp: DateTime.now(),
    ));
  }

  void _sendMessage(String text) {
    if (text.trim().isEmpty) return;

    setState(() {
      _messages.add(ChatMessage(
        text: text,
        isUser: true,
        timestamp: DateTime.now(),
      ));
      _isTyping = true;
    });
    _textController.clear();
    _scrollToBottom();

    // Simulate bot reply
    Future.delayed(const Duration(milliseconds: 1500), () {
      if (!mounted) return;
      
      String botReply = _botResponses[_botResponseIndex % _botResponses.length];
      _botResponseIndex++;

      setState(() {
        _isTyping = false;
        _messages.add(ChatMessage(
          text: botReply,
          isUser: false,
          timestamp: DateTime.now(),
        ));
      });
      _scrollToBottom();
    });
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  Widget _buildMessageContent(String text) {
    final spans = <TextSpan>[];
    final lowerText = text.toLowerCase();
    final matches = <Map<String, dynamic>>[];

    // Match terms
    for (var vocab in widget.track.sampleVocabulary) {
      final termStr = vocab.term.toLowerCase();
      int index = 0;
      while (true) {
        index = lowerText.indexOf(termStr, index);
        if (index == -1) break;
        matches.add({
          'start': index,
          'end': index + termStr.length,
          'vocab': vocab,
        });
        index += termStr.length;
      }
    }

    // Sort by start position
    matches.sort((a, b) => a['start'].compareTo(b['start']));

    // Filter overlapping matches
    final cleanMatches = <Map<String, dynamic>>[];
    int lastEnd = 0;
    for (var m in matches) {
      if (m['start'] >= lastEnd) {
        cleanMatches.add(m);
        lastEnd = m['end'];
      }
    }

    // Build rich text spans
    int currentPos = 0;
    for (var m in cleanMatches) {
      if (m['start'] > currentPos) {
        spans.add(TextSpan(
          text: text.substring(currentPos, m['start']),
          style: const TextStyle(color: Colors.white),
        ));
      }

      final VocabTerm vocab = m['vocab'];
      spans.add(TextSpan(
        text: text.substring(m['start'], m['end']),
        style: TextStyle(
          color: widget.track.accentColor,
          fontWeight: FontWeight.bold,
          decoration: TextDecoration.underline,
        ),
      ));
      currentPos = m['end'];
    }

    if (currentPos < text.length) {
      spans.add(TextSpan(
        text: text.substring(currentPos),
        style: const TextStyle(color: Colors.white),
      ));
    }

    if (spans.isEmpty) {
      return Text(
        text,
        style: AppTheme.bodyMedium.copyWith(color: Colors.white, height: 1.4),
      );
    }

    return RichText(
      text: TextSpan(
        style: AppTheme.bodyMedium.copyWith(height: 1.4),
        children: spans,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(gradient: AppTheme.backgroundGradient),
        child: SafeArea(
          child: Column(
            children: [
              const SizedBox(height: 12),
              
              // ── Header / Top Bar ──
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Row(
                  children: [
                    IconButton(
                      icon: const Icon(Icons.arrow_back_ios_new_rounded, color: Colors.white),
                      onPressed: () => Navigator.of(context).pop(),
                    ),
                    const SizedBox(width: 8),
                    // Coach Avatar
                    Container(
                      width: 44,
                      height: 44,
                      decoration: BoxDecoration(
                        gradient: AppTheme.buttonGradient(widget.track.accentColor),
                        shape: BoxShape.circle,
                        boxShadow: [
                          BoxShadow(
                            color: widget.track.accentColor.withValues(alpha: 0.3),
                            blurRadius: 10,
                            offset: const Offset(0, 4),
                          )
                        ],
                      ),
                      child: Icon(_botIcon, color: Colors.white, size: 22),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Text(
                                _botName,
                                style: AppTheme.labelBold.copyWith(color: Colors.white),
                              ),
                              const SizedBox(width: 6),
                              // Pulsing Green Dot
                              Container(
                                width: 8,
                                height: 8,
                                decoration: const BoxDecoration(
                                  color: AppTheme.successGreen,
                                  shape: BoxShape.circle,
                                ),
                              ).animate(onPlay: (controller) => controller.repeat(reverse: true))
                               .fade(duration: 800.ms, begin: 0.3, end: 1.0),
                            ],
                          ),
                          const SizedBox(height: 2),
                          Text(
                            _botTitle,
                            style: AppTheme.bodySmall.copyWith(fontSize: 11),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ).animate().fadeIn(duration: 400.ms),

              const SizedBox(height: 12),
              const Divider(color: Colors.white10, height: 1),

              // ── Chat Messages List ──
              Expanded(
                child: ListView.builder(
                  controller: _scrollController,
                  padding: const EdgeInsets.all(20),
                  itemCount: _messages.length + (_isTyping ? 1 : 0),
                  itemBuilder: (context, index) {
                    if (index == _messages.length && _isTyping) {
                      return _buildTypingBubble();
                    }
                    
                    final msg = _messages[index];
                    return _buildChatBubble(msg);
                  },
                ),
              ),

              // ── Quick Reply Chips ──
              if (_messages.isNotEmpty && _messages.last.isUser == false && !_isTyping)
                SizedBox(
                  height: 48,
                  child: ListView.builder(
                    scrollDirection: Axis.horizontal,
                    padding: const EdgeInsets.symmetric(horizontal: 16),
                    itemCount: _quickReplies.length,
                    itemBuilder: (context, index) {
                      final reply = _quickReplies[index];
                      return Padding(
                        padding: const EdgeInsets.only(right: 8, bottom: 8),
                        child: ActionChip(
                          label: Text(reply),
                          onPressed: () => _sendMessage(reply),
                          backgroundColor: Colors.white.withValues(alpha: 0.05),
                          labelStyle: AppTheme.bodySmall.copyWith(
                            color: Colors.white70,
                          ),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                            side: BorderSide(
                              color: Colors.white.withValues(alpha: 0.1),
                            ),
                          ),
                        ),
                      );
                    },
                  ),
                ).animate().fadeIn(duration: 300.ms),

              // ── Bottom Input Field ──
              Padding(
                padding: const EdgeInsets.all(16),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                  decoration: AppTheme.glassDecoration(
                    borderRadius: 24,
                    borderColor: Colors.white.withValues(alpha: 0.1),
                  ),
                  child: Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: _textController,
                          style: AppTheme.bodyMedium.copyWith(color: Colors.white),
                          cursorColor: widget.track.accentColor,
                          decoration: InputDecoration(
                            hintText: 'Type your response...',
                            hintStyle: AppTheme.bodyMedium.copyWith(
                              color: AppTheme.textMuted,
                            ),
                            border: InputBorder.none,
                          ),
                          onSubmitted: _sendMessage,
                        ),
                      ),
                      IconButton(
                        icon: Icon(Icons.send_rounded, color: widget.track.accentColor),
                        onPressed: () => _sendMessage(_textController.text),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildChatBubble(ChatMessage message) {
    final isUser = message.isUser;
    
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 16),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.75,
        ),
        decoration: isUser
            ? BoxDecoration(
                gradient: AppTheme.buttonGradient(widget.track.accentColor),
                borderRadius: const BorderRadius.only(
                  topLeft: Radius.circular(16),
                  topRight: Radius.circular(16),
                  bottomLeft: Radius.circular(16),
                  bottomRight: Radius.circular(4),
                ),
                boxShadow: [
                  BoxShadow(
                    color: widget.track.accentColor.withValues(alpha: 0.2),
                    blurRadius: 8,
                    offset: const Offset(0, 4),
                  ),
                ],
              )
            : AppTheme.glassDecoration(
                borderRadius: const BorderRadius.only(
                  topLeft: Radius.circular(16),
                  topRight: Radius.circular(16),
                  bottomLeft: Radius.circular(4),
                  bottomRight: Radius.circular(16),
                ),
                borderColor: Colors.white.withValues(alpha: 0.05),
                opacity: 0.08,
              ),
        child: isUser
            ? Text(
                message.text,
                style: AppTheme.bodyMedium.copyWith(color: Colors.white, height: 1.4),
              )
            : _buildMessageContent(message.text),
      ).animate().slideY(
            begin: 0.1,
            end: 0,
            duration: 250.ms,
            curve: Curves.easeOutQuad,
          ),
    );
  }

  Widget _buildTypingBubble() {
    return Align(
      alignment: Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 16),
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
        decoration: AppTheme.glassDecoration(
          borderRadius: const BorderRadius.only(
            topLeft: Radius.circular(16),
            topRight: Radius.circular(16),
            bottomLeft: Radius.circular(4),
            bottomRight: Radius.circular(16),
          ),
          borderColor: Colors.white.withValues(alpha: 0.05),
          opacity: 0.08,
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: List.generate(3, (index) {
            return Container(
              margin: const EdgeInsets.symmetric(horizontal: 2),
              width: 6,
              height: 6,
              decoration: BoxDecoration(
                color: widget.track.accentColor.withValues(alpha: 0.6),
                shape: BoxShape.circle,
              ),
            ).animate(onPlay: (controller) => controller.repeat(reverse: true))
             .fade(duration: 400.ms, delay: (index * 150).ms, begin: 0.2, end: 1.0)
             .slideY(duration: 400.ms, delay: (index * 150).ms, begin: 0.2, end: -0.2);
          }),
        ),
      ),
    );
  }
}
