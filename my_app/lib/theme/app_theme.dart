import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  // ── Core Colors ──
  static const Color backgroundDark = Color(0xFF0A0E21);
  static const Color backgroundMid = Color(0xFF111633);
  static const Color surfaceCard = Color(0xFF1C2043);
  static const Color primaryAccent = Color(0xFF6C63FF);
  static const Color secondaryAccent = Color(0xFFFF6B6B);
  static const Color successGreen = Color(0xFF00D09C);
  static const Color textPrimary = Color(0xFFFFFFFF);
  static const Color textSecondary = Color(0xFFA0A3BD);
  static const Color textMuted = Color(0xFF6B6F8D);

  // ── Track-specific accent colors ──
  static const Color trackStartup = Color(0xFFFF6B6B);
  static const Color trackTech = Color(0xFF4FC3F7);
  static const Color trackBusiness = Color(0xFFAB6CFF);

  // ── Gradients ──
  static const LinearGradient backgroundGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [backgroundDark, Color(0xFF0D1137), backgroundMid],
  );

  static const LinearGradient primaryGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFF6C63FF), Color(0xFF4834DF)],
  );

  static const LinearGradient accentGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFFFF6B6B), Color(0xFFFF8E53)],
  );

  static LinearGradient buttonGradient(Color accentColor) {
    return LinearGradient(
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
      colors: [
        accentColor,
        accentColor.withValues(alpha: 0.8),
      ],
    );
  }

  // ── Glassmorphism decoration ──
  static BoxDecoration glassDecoration({
    Color? borderColor,
    dynamic borderRadius = 20.0,
    double opacity = 0.08,
  }) {
    BorderRadiusGeometry r;
    if (borderRadius is num) {
      r = BorderRadius.circular(borderRadius.toDouble());
    } else {
      r = borderRadius as BorderRadiusGeometry;
    }
    return BoxDecoration(
      color: Colors.white.withValues(alpha: opacity),
      borderRadius: r,
      border: Border.all(
        color: borderColor ?? Colors.white.withValues(alpha: 0.12),
        width: 1,
      ),
    );
  }

  // ── Text Styles ──
  static TextStyle get headingLarge => GoogleFonts.outfit(
        fontSize: 32,
        fontWeight: FontWeight.w700,
        color: textPrimary,
        height: 1.2,
      );

  static TextStyle get headingMedium => GoogleFonts.outfit(
        fontSize: 24,
        fontWeight: FontWeight.w600,
        color: textPrimary,
        height: 1.3,
      );

  static TextStyle get headingSmall => GoogleFonts.outfit(
        fontSize: 18,
        fontWeight: FontWeight.w600,
        color: textPrimary,
      );

  static TextStyle get bodyLarge => GoogleFonts.inter(
        fontSize: 16,
        fontWeight: FontWeight.w400,
        color: textSecondary,
        height: 1.6,
      );

  static TextStyle get bodyMedium => GoogleFonts.inter(
        fontSize: 14,
        fontWeight: FontWeight.w400,
        color: textSecondary,
        height: 1.5,
      );

  static TextStyle get bodySmall => GoogleFonts.inter(
        fontSize: 12,
        fontWeight: FontWeight.w400,
        color: textMuted,
      );

  static TextStyle get labelBold => GoogleFonts.inter(
        fontSize: 14,
        fontWeight: FontWeight.w600,
        color: textPrimary,
      );

  static TextStyle get buttonText => GoogleFonts.inter(
        fontSize: 16,
        fontWeight: FontWeight.w600,
        color: textPrimary,
        letterSpacing: 0.5,
      );

  // ── ThemeData ──
  static ThemeData get darkTheme => ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: backgroundDark,
        colorScheme: const ColorScheme.dark(
          primary: primaryAccent,
          secondary: secondaryAccent,
          surface: surfaceCard,
        ),
        textTheme: GoogleFonts.interTextTheme(ThemeData.dark().textTheme),
        useMaterial3: true,
      );
}
