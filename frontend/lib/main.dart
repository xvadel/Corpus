import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'theme/app_theme.dart';
import 'models/track.dart';
import 'screens/splash_screen.dart';
import 'screens/onboarding_screen.dart';
import 'screens/home_screen.dart';
import 'screens/vocabulary_screen.dart';
import 'screens/chat_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
  runApp(const CorpusApp());
}

class CorpusApp extends StatelessWidget {
  const CorpusApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Corpus',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: AppTheme.backgroundDark,
        fontFamily: 'Inter',
        useMaterial3: true,
      ),
      initialRoute: '/',
      onGenerateRoute: (settings) {
        switch (settings.name) {
          case '/':
            return MaterialPageRoute(builder: (context) => const SplashScreen());
          case '/onboarding':
            return MaterialPageRoute(builder: (context) => const OnboardingScreen());
          case '/home':
            final track = settings.arguments as Track;
            return MaterialPageRoute(builder: (context) => HomeScreen(track: track));
          case '/vocabulary':
            final track = settings.arguments as Track;
            return MaterialPageRoute(builder: (context) => VocabularyScreen(track: track));
          case '/chat':
            final track = settings.arguments as Track;
            return MaterialPageRoute(builder: (context) => ChatScreen(track: track));
          default:
            return MaterialPageRoute(
              builder: (context) => const Scaffold(
                body: Center(
                  child: Text('Route not found'),
                ),
              ),
            );
        }
      },
    );
  }
}
