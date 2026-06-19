import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../theme/app_theme.dart';
import '../models/track.dart';

class HomeScreen extends StatelessWidget {
  final Track track;

  const HomeScreen({super.key, required this.track});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(gradient: AppTheme.backgroundGradient),
        child: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 24),

                // ── Top Bar ──
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Hello, Learner 👋', style: AppTheme.bodyMedium),
                        const SizedBox(height: 4),
                        Text(track.name, style: AppTheme.headingMedium),
                      ],
                    ),
                    GestureDetector(
                      onTap: () {
                        Navigator.of(context).pushReplacementNamed('/onboarding');
                      },
                      child: Container(
                        padding: const EdgeInsets.all(10),
                        decoration: AppTheme.glassDecoration(borderRadius: 14),
                        child: Icon(
                          Icons.swap_horiz_rounded,
                          color: track.accentColor,
                          size: 22,
                        ),
                      ),
                    ),
                  ],
                ).animate().fadeIn(duration: 400.ms),

                const SizedBox(height: 28),

                // ── Stats Row ──
                Row(
                  children: [
                    _StatTile(
                      label: 'Words',
                      value: '${track.sampleVocabulary.length}',
                      icon: Icons.menu_book_rounded,
                      color: track.accentColor,
                    ),
                    const SizedBox(width: 12),
                    _StatTile(
                      label: 'Streak',
                      value: '1 🔥',
                      icon: Icons.local_fire_department_rounded,
                      color: AppTheme.secondaryAccent,
                    ),
                    const SizedBox(width: 12),
                    _StatTile(
                      label: 'Level',
                      value: 'Starter',
                      icon: Icons.emoji_events_rounded,
                      color: AppTheme.successGreen,
                    ),
                  ],
                )
                    .animate(delay: 200.ms)
                    .fadeIn(duration: 500.ms)
                    .slideY(begin: 0.1, end: 0, duration: 500.ms),

                const SizedBox(height: 32),

                // ── Section: Quick Actions ──
                Text('Continue Learning', style: AppTheme.headingSmall)
                    .animate(delay: 350.ms)
                    .fadeIn(duration: 400.ms),

                const SizedBox(height: 16),

                // Action cards
                _ActionCard(
                  title: 'Practice Vocabulary',
                  subtitle: 'Master ${track.sampleVocabulary.length} key terms in your field',
                  icon: Icons.style_rounded,
                  accentColor: track.accentColor,
                  onTap: () {
                    Navigator.of(context).pushNamed(
                      '/vocabulary',
                      arguments: track,
                    );
                  },
                )
                    .animate(delay: 450.ms)
                    .fadeIn(duration: 500.ms)
                    .slideX(begin: 0.05, end: 0, duration: 500.ms),

                const SizedBox(height: 12),

                _ActionCard(
                  title: 'Pitch Simulator',
                  subtitle: 'Roleplay a live conversation with an AI coach',
                  icon: Icons.record_voice_over_rounded,
                  accentColor: AppTheme.secondaryAccent,
                  onTap: () {
                    Navigator.of(context).pushNamed(
                      '/chat',
                      arguments: track,
                    );
                  },
                )
                    .animate(delay: 600.ms)
                    .fadeIn(duration: 500.ms)
                    .slideX(begin: 0.05, end: 0, duration: 500.ms),

                const SizedBox(height: 12),

                _ActionCard(
                  title: 'Grammar Coach',
                  subtitle: 'Get real-time corrections on your professional writing',
                  icon: Icons.spellcheck_rounded,
                  accentColor: AppTheme.successGreen,
                  isComingSoon: true,
                  onTap: () {},
                )
                    .animate(delay: 750.ms)
                    .fadeIn(duration: 500.ms)
                    .slideX(begin: 0.05, end: 0, duration: 500.ms),

                const SizedBox(height: 32),

                // ── Focus Areas ──
                Text('Your Focus Areas', style: AppTheme.headingSmall)
                    .animate(delay: 850.ms)
                    .fadeIn(duration: 400.ms),

                const SizedBox(height: 12),

                Wrap(
                  spacing: 10,
                  runSpacing: 10,
                  children: track.focusAreas.map((area) {
                    return Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 10,
                      ),
                      decoration: BoxDecoration(
                        color: track.accentColor.withValues(alpha: 0.1),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(
                          color: track.accentColor.withValues(alpha: 0.25),
                        ),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(
                            Icons.check_circle_rounded,
                            size: 16,
                            color: track.accentColor,
                          ),
                          const SizedBox(width: 8),
                          Text(
                            area,
                            style: AppTheme.labelBold.copyWith(
                              color: track.accentColor,
                            ),
                          ),
                        ],
                      ),
                    );
                  }).toList(),
                )
                    .animate(delay: 950.ms)
                    .fadeIn(duration: 500.ms),

                const SizedBox(height: 40),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

// ── Stat Tile Widget ──
class _StatTile extends StatelessWidget {
  final String label;
  final String value;
  final IconData icon;
  final Color color;

  const _StatTile({
    required this.label,
    required this.value,
    required this.icon,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: AppTheme.glassDecoration(),
        child: Column(
          children: [
            Icon(icon, color: color, size: 22),
            const SizedBox(height: 8),
            Text(
              value,
              style: AppTheme.headingSmall.copyWith(fontSize: 16),
            ),
            const SizedBox(height: 2),
            Text(label, style: AppTheme.bodySmall),
          ],
        ),
      ),
    );
  }
}

// ── Action Card Widget ──
class _ActionCard extends StatelessWidget {
  final String title;
  final String subtitle;
  final IconData icon;
  final Color accentColor;
  final VoidCallback onTap;
  final bool isComingSoon;

  const _ActionCard({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.accentColor,
    required this.onTap,
    this.isComingSoon = false,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: isComingSoon ? null : onTap,
      child: Opacity(
        opacity: isComingSoon ? 0.5 : 1.0,
        child: Container(
          padding: const EdgeInsets.all(18),
          decoration: AppTheme.glassDecoration(
            borderColor: accentColor.withValues(alpha: 0.2),
          ),
          child: Row(
            children: [
              Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  color: accentColor.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Icon(icon, color: accentColor, size: 24),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Text(title, style: AppTheme.labelBold),
                        if (isComingSoon) ...[
                          const SizedBox(width: 8),
                          Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 8,
                              vertical: 2,
                            ),
                            decoration: BoxDecoration(
                              color: AppTheme.textMuted.withValues(alpha: 0.2),
                              borderRadius: BorderRadius.circular(6),
                            ),
                            child: Text(
                              'Soon',
                              style: AppTheme.bodySmall.copyWith(fontSize: 10),
                            ),
                          ),
                        ],
                      ],
                    ),
                    const SizedBox(height: 4),
                    Text(
                      subtitle,
                      style: AppTheme.bodySmall,
                      maxLines: 2,
                    ),
                  ],
                ),
              ),
              if (!isComingSoon)
                Icon(
                  Icons.arrow_forward_ios_rounded,
                  color: AppTheme.textMuted,
                  size: 14,
                ),
            ],
          ),
        ),
      ),
    );
  }
}
