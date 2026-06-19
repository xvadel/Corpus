import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class Track {
  final String id;
  final String name;
  final String description;
  final IconData icon;
  final Color accentColor;
  final List<String> focusAreas;
  final List<VocabTerm> sampleVocabulary;

  const Track({
    required this.id,
    required this.name,
    required this.description,
    required this.icon,
    required this.accentColor,
    required this.focusAreas,
    required this.sampleVocabulary,
  });
}

class VocabTerm {
  final String term;
  final String definition;
  final String example;
  final String category;

  const VocabTerm({
    required this.term,
    required this.definition,
    required this.example,
    required this.category,
  });
}

// ── Hardcoded track data (matches config.toml) ──

final List<Track> allTracks = [
  Track(
    id: 'startup_pitching',
    name: 'Startup & Venture Capital',
    description:
        'Learn to pitch ideas to investors, negotiate term sheets, and handle tough Q&A sessions.',
    icon: Icons.rocket_launch_rounded,
    accentColor: AppTheme.trackStartup,
    focusAreas: ['Investor Pitching', 'Financial Terminology', 'Confidence & Delivery'],
    sampleVocabulary: [
      const VocabTerm(
        term: 'Burn Rate',
        definition: 'The rate at which a startup spends its capital before generating positive cash flow.',
        example: '"Our current burn rate is \$50K per month, giving us 14 months of runway."',
        category: 'Finance',
      ),
      const VocabTerm(
        term: 'Runway',
        definition: 'The amount of time a company can continue operating before running out of money.',
        example: '"With the seed round, we extended our runway to 18 months."',
        category: 'Finance',
      ),
      const VocabTerm(
        term: 'Traction',
        definition: 'Measurable evidence of market demand — users, revenue, growth rate.',
        example: '"We have strong traction with 10K monthly active users growing 20% month-over-month."',
        category: 'Pitching',
      ),
      const VocabTerm(
        term: 'Valuation',
        definition: 'The estimated worth of a company, often used during fundraising negotiations.',
        example: '"We are raising at a pre-money valuation of \$5 million."',
        category: 'Finance',
      ),
      const VocabTerm(
        term: 'Cap Table',
        definition: 'A spreadsheet showing the equity ownership, dilution, and value of shares in a company.',
        example: '"Let me walk you through our cap table to show the current ownership structure."',
        category: 'Legal',
      ),
      const VocabTerm(
        term: 'Term Sheet',
        definition: 'A non-binding agreement outlining the basic terms of an investment deal.',
        example: '"We received a term sheet from Sequoia with a \$2M investment at 15% equity."',
        category: 'Legal',
      ),
      const VocabTerm(
        term: 'Due Diligence',
        definition: 'The investigation process investors conduct before finalizing a deal.',
        example: '"The VC firm is currently in the due diligence phase, reviewing our financials."',
        category: 'Process',
      ),
      const VocabTerm(
        term: 'Pivot',
        definition: 'A fundamental change in a startup\'s business model or product strategy.',
        example: '"After analyzing user feedback, we decided to pivot from B2C to B2B."',
        category: 'Strategy',
      ),
    ],
  ),
  Track(
    id: 'software_engineering',
    name: 'Software Engineering & Tech',
    description:
        'Master technical communication during system design, standups, code reviews, and interviews.',
    icon: Icons.code_rounded,
    accentColor: AppTheme.trackTech,
    focusAreas: ['System Design', 'Agile Communication', 'Explaining Technical Concepts'],
    sampleVocabulary: [
      const VocabTerm(
        term: 'Microservices',
        definition: 'An architectural style where an application is composed of small, independent services.',
        example: '"We decomposed the monolith into microservices to improve scalability."',
        category: 'Architecture',
      ),
      const VocabTerm(
        term: 'API Gateway',
        definition: 'A server that acts as a single entry point for a set of microservices.',
        example: '"All client requests are routed through our API gateway for authentication."',
        category: 'Architecture',
      ),
      const VocabTerm(
        term: 'Load Balancer',
        definition: 'A device or software that distributes network traffic across multiple servers.',
        example: '"We use a load balancer to distribute traffic evenly across three servers."',
        category: 'Infrastructure',
      ),
      const VocabTerm(
        term: 'CI/CD',
        definition: 'Continuous Integration / Continuous Deployment — automating build, test, and release.',
        example: '"Our CI/CD pipeline runs unit tests and deploys to staging on every pull request."',
        category: 'DevOps',
      ),
      const VocabTerm(
        term: 'Technical Debt',
        definition: 'The implied cost of rework caused by choosing quick solutions over sustainable ones.',
        example: '"We need to allocate two sprints to address the technical debt in the payment module."',
        category: 'Process',
      ),
      const VocabTerm(
        term: 'Latency',
        definition: 'The time delay between a request and its response in a system.',
        example: '"We reduced API latency from 400ms to 120ms by implementing caching."',
        category: 'Performance',
      ),
      const VocabTerm(
        term: 'Scalability',
        definition: 'The ability of a system to handle increasing workloads by adding resources.',
        example: '"The system is designed for horizontal scalability using Kubernetes."',
        category: 'Architecture',
      ),
      const VocabTerm(
        term: 'Refactoring',
        definition: 'Restructuring existing code without changing its external behavior.',
        example: '"I spent the sprint refactoring the authentication module to improve readability."',
        category: 'Process',
      ),
    ],
  ),
  Track(
    id: 'business_product',
    name: 'Business & Product Management',
    description:
        'Communicate effectively with cross-functional teams, stakeholders, and enterprise clients.',
    icon: Icons.business_center_rounded,
    accentColor: AppTheme.trackBusiness,
    focusAreas: ['Stakeholder Alignment', 'Product Discovery', 'Metrics & KPI Reporting'],
    sampleVocabulary: [
      const VocabTerm(
        term: 'KPI',
        definition: 'Key Performance Indicator — a measurable value that shows how effectively goals are achieved.',
        example: '"Our primary KPI for Q3 is a 15% increase in user retention rate."',
        category: 'Metrics',
      ),
      const VocabTerm(
        term: 'ROI',
        definition: 'Return on Investment — the ratio of net profit to the cost of investment.',
        example: '"The marketing campaign delivered a 3.5x ROI within the first quarter."',
        category: 'Finance',
      ),
      const VocabTerm(
        term: 'Stakeholder',
        definition: 'Any person or group with an interest or concern in a project or business.',
        example: '"We need to align with all stakeholders before proceeding with the redesign."',
        category: 'Communication',
      ),
      const VocabTerm(
        term: 'Go-to-Market',
        definition: 'A strategy plan for launching a product to market, including pricing, distribution, and messaging.',
        example: '"Our go-to-market strategy focuses on enterprise clients in the healthcare sector."',
        category: 'Strategy',
      ),
      const VocabTerm(
        term: 'Churn Rate',
        definition: 'The percentage of customers who stop using a product over a given period.',
        example: '"We reduced our monthly churn rate from 8% to 4.5% by improving onboarding."',
        category: 'Metrics',
      ),
      const VocabTerm(
        term: 'Sprint',
        definition: 'A fixed time period (usually 1-2 weeks) in which a set of tasks must be completed.',
        example: '"In this sprint, we are focusing on the checkout flow and payment integration."',
        category: 'Agile',
      ),
      const VocabTerm(
        term: 'Deliverable',
        definition: 'A tangible or intangible output produced as the result of a project.',
        example: '"The key deliverable for this milestone is a working prototype of the dashboard."',
        category: 'Project Management',
      ),
      const VocabTerm(
        term: 'Roadmap',
        definition: 'A strategic plan that outlines the vision, direction, and milestones for a product.',
        example: '"According to our product roadmap, the mobile app launch is scheduled for Q2."',
        category: 'Strategy',
      ),
    ],
  ),
];
