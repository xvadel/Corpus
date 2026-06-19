import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../theme/app_theme.dart';
import '../models/track.dart';
import '../widgets/track_card.dart';

class OnboardingScreen extends StatelessWidget {
  const OnboardingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(gradient: AppTheme.backgroundGradient),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 40),

                // Header
                Text(
                  'Welcome to Corpus 👋',
                  style: AppTheme.headingLarge,
                ).animate().fadeIn(duration: 500.ms).slideX(
                      begin: -0.1,
                      end: 0,
                      duration: 500.ms,
                    ),

                const SizedBox(height: 12),

                Text(
                  'What do you need to master?',
                  style: AppTheme.bodyLarge,
                ).animate(delay: 200.ms).fadeIn(duration: 500.ms),

                const SizedBox(height: 8),

                Text(
                  'Choose your career track and we\'ll build your personalized vocabulary, grammar drills, and roleplay simulations.',
                  style: AppTheme.bodyMedium,
                ).animate(delay: 350.ms).fadeIn(duration: 500.ms),

                const SizedBox(height: 32),

                // Track cards
                Expanded(
                  child: ListView.builder(
                    itemCount: allTracks.length,
                    itemBuilder: (context, index) {
                      final track = allTracks[index];
                      return TrackCard(
                        track: track,
                        onTap: () {
                          Navigator.of(context).pushReplacementNamed(
                            '/home',
                            arguments: track,
                          );
                        },
                      )
                          .animate(delay: Duration(milliseconds: 400 + (index * 150)))
                          .fadeIn(duration: 500.ms)
                          .slideY(begin: 0.15, end: 0, duration: 500.ms);
                    },
                  ),
                ),

                // Footer
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  child: Center(
                    child: Text(
                      'You can always change your track later',
                      style: AppTheme.bodySmall.copyWith(
                        fontStyle: FontStyle.italic,
                      ),
                    ),
                  ),
                ).animate(delay: 1000.ms).fadeIn(duration: 500.ms),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
