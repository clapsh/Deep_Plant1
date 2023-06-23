import 'package:deep_plant_1/pages/home_page.dart';
import 'package:deep_plant_1/pages/logged_in_page.dart';
import 'package:deep_plant_1/pages/sign_in_page.dart';
import 'package:deep_plant_1/pages/sign_up_page.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(const MyApp());
}

final _router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomePage(),
      routes: [
        GoRoute(
          path: 'sign-in',
          builder: (context, state) => const SignIn(),
          routes: [
            GoRoute(
              path: 'sign-up',
              builder: (context, state) => const SignUp(),
            ),
          ],
        ),
      ],
    ),
    GoRoute(
      path: '/logged-in',
      builder: (context, state) => const LoggedInPage(),
    ),
  ],
);

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'DeepPlant-demo',
      theme: ThemeData(
        primaryColor: const Color.fromRGBO(51, 51, 51, 1),
        buttonTheme:
            const ButtonThemeData(buttonColor: Color.fromRGBO(51, 51, 51, 1)),
      ),
      routerConfig: _router,
    );
  }
}
