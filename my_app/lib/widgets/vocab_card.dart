import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../models/track.dart';

class VocabCard extends StatefulWidget {
  final VocabTerm term;
  final Color accentColor;

  const VocabCard({
    super.key,
    required this.term,
    required this.accentColor,
  });

  @override
  State<VocabCard> createState() => _VocabCardState();
}

class _VocabCardState extends State<VocabCard>
    with SingleTickerProviderStateMixin {
  bool _isFlipped = false;
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 400),
    );
    _animation = Tween<double>(begin: 0, end: 1).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOutCubic),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _flip() {
    if (_isFlipped) {
      _controller.reverse();
    } else {
      _controller.forward();
    }
    setState(() => _isFlipped = !_isFlipped);
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _flip,
      child: AnimatedBuilder(
        animation: _animation,
        builder: (context, child) {
          final angle = _animation.value * 3.14159;
          final isFront = _animation.value < 0.5;

          return Transform(
            alignment: Alignment.center,
            transform: Matrix4.identity()
              ..setEntry(3, 2, 0.001)
              ..rotateY(angle),
            child: isFront ? _buildFront() : _buildBack(),
          );
        },
      ),
    );
  }

  Widget _buildFront() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: AppTheme.glassDecoration(
        borderColor: widget.accentColor.withValues(alpha: 0.2),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          // Category chip
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
            decoration: BoxDecoration(
              color: widget.accentColor.withValues(alpha: 0.15),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(
              widget.term.category,
              style: AppTheme.bodySmall.copyWith(
                color: widget.accentColor,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
          const SizedBox(height: 14),
          // Term
          Text(
            widget.term.term,
            style: AppTheme.headingMedium.copyWith(
              color: Colors.white,
            ),
          ),
          const SizedBox(height: 10),
          // Tap hint
          Row(
            children: [
              Icon(
                Icons.touch_app_rounded,
                color: AppTheme.textMuted,
                size: 16,
              ),
              const SizedBox(width: 6),
              Text(
                'Tap to reveal definition',
                style: AppTheme.bodySmall.copyWith(
                  fontStyle: FontStyle.italic,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildBack() {
    return Transform(
      alignment: Alignment.center,
      transform: Matrix4.identity()..rotateY(3.14159),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(20),
        decoration: AppTheme.glassDecoration(
          borderColor: widget.accentColor.withValues(alpha: 0.3),
          opacity: 0.12,
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Definition header
            Text(
              'Definition',
              style: AppTheme.labelBold.copyWith(
                color: widget.accentColor,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              widget.term.definition,
              style: AppTheme.bodyMedium.copyWith(
                color: Colors.white.withValues(alpha: 0.9),
              ),
            ),
            const SizedBox(height: 16),
            // Example
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.white.withValues(alpha: 0.05),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(
                  color: Colors.white.withValues(alpha: 0.08),
                ),
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(
                    Icons.format_quote_rounded,
                    color: widget.accentColor.withValues(alpha: 0.6),
                    size: 18,
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      widget.term.example,
                      style: AppTheme.bodySmall.copyWith(
                        color: Colors.white.withValues(alpha: 0.7),
                        fontStyle: FontStyle.italic,
                        height: 1.5,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
