import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../theme/app_theme.dart';
import '../models/track.dart';
import '../widgets/vocab_card.dart';

class VocabularyScreen extends StatefulWidget {
  final Track track;

  const VocabularyScreen({super.key, required this.track});

  @override
  State<VocabularyScreen> createState() => _VocabularyScreenState();
}

class _VocabularyScreenState extends State<VocabularyScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  int _currentIndex = 0;
  final PageController _pageController = PageController();
  String _selectedCategory = 'All';

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // Get unique categories
    final categories = ['All', ...widget.track.sampleVocabulary.map((t) => t.category).toSet().toList()];
    
    // Filtered terms
    final filteredTerms = _selectedCategory == 'All'
        ? widget.track.sampleVocabulary
        : widget.track.sampleVocabulary.where((t) => t.category == _selectedCategory).toList();

    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(gradient: AppTheme.backgroundGradient),
        child: SafeArea(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 16),
              
              // ── Header ──
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                child: Row(
                  children: [
                    IconButton(
                      icon: const Icon(Icons.arrow_back_ios_new_rounded, color: Colors.white),
                      onPressed: () => Navigator.of(context).pop(),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            widget.track.name,
                            style: AppTheme.bodySmall.copyWith(color: widget.track.accentColor),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            'Vocabulary Deck',
                            style: AppTheme.headingMedium,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ).animate().fadeIn(duration: 400.ms),

              const SizedBox(height: 16),

              // ── Tab Bar ──
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                child: Container(
                  height: 48,
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: 0.05),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.white.withValues(alpha: 0.08)),
                  ),
                  child: TabBar(
                    controller: _tabController,
                    indicator: BoxDecoration(
                      color: widget.track.accentColor.withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: widget.track.accentColor.withValues(alpha: 0.3)),
                    ),
                    indicatorSize: TabBarIndicatorSize.tab,
                    labelColor: Colors.white,
                    unselectedLabelColor: AppTheme.textMuted,
                    labelStyle: AppTheme.labelBold,
                    unselectedLabelStyle: AppTheme.bodyMedium,
                    tabs: const [
                      Tab(text: 'Flashcards'),
                      Tab(text: 'All Terms'),
                    ],
                  ),
                ),
              ).animate(delay: 150.ms).fadeIn(),

              const SizedBox(height: 16),

              // ── Category Selector (Chips) ──
              SizedBox(
                height: 40,
                child: ListView.builder(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.symmetric(horizontal: 20),
                  itemCount: categories.length,
                  itemBuilder: (context, index) {
                    final cat = categories[index];
                    final isSelected = _selectedCategory == cat;
                    return Padding(
                      padding: const EdgeInsets.only(right: 8),
                      child: ChoiceChip(
                        label: Text(cat),
                        selected: isSelected,
                        onSelected: (selected) {
                          setState(() {
                            _selectedCategory = cat;
                            _currentIndex = 0;
                            if (_pageController.hasClients) {
                              _pageController.jumpToPage(0);
                            }
                          });
                        },
                        selectedColor: widget.track.accentColor.withValues(alpha: 0.25),
                        backgroundColor: Colors.white.withValues(alpha: 0.05),
                        labelStyle: AppTheme.bodySmall.copyWith(
                          color: isSelected ? Colors.white : AppTheme.textMuted,
                          fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                        ),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(20),
                          side: BorderSide(
                            color: isSelected
                                ? widget.track.accentColor.withValues(alpha: 0.5)
                                : Colors.white.withValues(alpha: 0.08),
                          ),
                        ),
                      ),
                    );
                  },
                ),
              ).animate(delay: 250.ms).fadeIn(),

              const SizedBox(height: 20),

              // ── Tab Bar View ──
              Expanded(
                child: TabBarView(
                  controller: _tabController,
                  children: [
                    // Flashcards View
                    filteredTerms.isEmpty
                        ? _buildEmptyState()
                        : _buildFlashcardsView(filteredTerms),

                    // All Terms View
                    filteredTerms.isEmpty
                        ? _buildEmptyState()
                        : _buildAllTermsView(filteredTerms),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.layers_clear_rounded, size: 64, color: AppTheme.textMuted),
          const SizedBox(height: 16),
          Text('No terms found in this category.', style: AppTheme.bodyMedium),
        ],
      ),
    );
  }

  Widget _buildFlashcardsView(List<VocabTerm> terms) {
    final clampedIndex = _currentIndex.clamp(0, terms.length - 1);
    
    return Column(
      children: [
        // Page view for flashcards
        Expanded(
          child: PageView.builder(
            controller: _pageController,
            itemCount: terms.length,
            onPageChanged: (index) {
              setState(() {
                _currentIndex = index;
              });
            },
            itemBuilder: (context, index) {
              return Padding(
                padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 10),
                child: VocabCard(
                  term: terms[index],
                  accentColor: widget.track.accentColor,
                ),
              );
            },
          ),
        ),

        const SizedBox(height: 20),

        // Indicator and navigation buttons
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              // Prev Button
              IconButton(
                icon: const Icon(Icons.arrow_back_rounded, color: Colors.white),
                onPressed: clampedIndex > 0
                    ? () {
                        _pageController.previousPage(
                          duration: const Duration(milliseconds: 300),
                          curve: Curves.easeInOut,
                        );
                      }
                    : null,
                style: IconButton.styleFrom(
                  backgroundColor: Colors.white.withValues(alpha: clampedIndex > 0 ? 0.08 : 0.02),
                  padding: const EdgeInsets.all(16),
                ),
              ),

              // Progress text & indicator
              Column(
                children: [
                  Text(
                    'Card ${clampedIndex + 1} of ${terms.length}',
                    style: AppTheme.bodyMedium.copyWith(fontWeight: FontWeight.w600),
                  ),
                  const SizedBox(height: 8),
                  Container(
                    width: 120,
                    height: 4,
                    decoration: BoxDecoration(
                      color: Colors.white.withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(2),
                    ),
                    child: Stack(
                      children: [
                        FractionallySizedBox(
                          widthFactor: terms.isNotEmpty ? (clampedIndex + 1) / terms.length : 0,
                          child: Container(
                            decoration: BoxDecoration(
                              color: widget.track.accentColor,
                              borderRadius: BorderRadius.circular(2),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),

              // Next Button
              IconButton(
                icon: const Icon(Icons.arrow_forward_rounded, color: Colors.white),
                onPressed: clampedIndex < terms.length - 1
                    ? () {
                        _pageController.nextPage(
                          duration: const Duration(milliseconds: 300),
                          curve: Curves.easeInOut,
                        );
                      }
                    : null,
                style: IconButton.styleFrom(
                  backgroundColor: Colors.white.withValues(alpha: clampedIndex < terms.length - 1 ? 0.08 : 0.02),
                  padding: const EdgeInsets.all(16),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildAllTermsView(List<VocabTerm> terms) {
    return ListView.builder(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 10),
      itemCount: terms.length,
      itemBuilder: (context, index) {
        final term = terms[index];
        return Padding(
          padding: const EdgeInsets.only(bottom: 12),
          child: Theme(
            data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
            child: Container(
              decoration: AppTheme.glassDecoration(
                borderColor: Colors.white.withValues(alpha: 0.08),
              ),
              child: ExpansionTile(
                title: Text(
                  term.term,
                  style: AppTheme.labelBold.copyWith(color: Colors.white),
                ),
                subtitle: Text(
                  term.category,
                  style: AppTheme.bodySmall.copyWith(color: widget.track.accentColor),
                ),
                trailing: const Icon(Icons.keyboard_arrow_down_rounded, color: Colors.white70),
                childrenPadding: const EdgeInsets.only(left: 16, right: 16, bottom: 16),
                expandedAlignment: Alignment.topLeft,
                children: [
                  Text(
                    'Definition:',
                    style: AppTheme.bodySmall.copyWith(
                      color: widget.track.accentColor,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    term.definition,
                    style: AppTheme.bodyMedium,
                  ),
                  const SizedBox(height: 12),
                  Text(
                    'Example:',
                    style: AppTheme.bodySmall.copyWith(
                      color: AppTheme.textMuted,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    term.example,
                    style: AppTheme.bodySmall.copyWith(
                      fontStyle: FontStyle.italic,
                      color: Colors.white.withValues(alpha: 0.7),
                    ),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}
