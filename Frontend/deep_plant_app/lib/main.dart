import 'package:deep_plant_app/models/user_model.dart';
import 'package:deep_plant_app/pages/sign-up/certification_page.dart';
import 'package:deep_plant_app/pages/home_page.dart';
import 'package:deep_plant_app/pages/sign-up/email_verification.dart';
import 'package:deep_plant_app/pages/sign-up/insertion_idnpw.dart';
import 'package:deep_plant_app/pages/logged_in_page.dart';
import 'package:deep_plant_app/pages/sign_in_page.dart';
import 'package:deep_plant_app/pages/sign-up/succeed_sign_up_page.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(const MyApp());
}

UserModel newUser = UserModel();

// 라우팅
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
              path: ('certification'),
              builder: (context, state) => Certification(
                user: newUser,
              ),
              routes: [
                GoRoute(
                  path: ('insert-id-pw'),
                  builder: (context, state) => InsertionIdnPw(
                    user: newUser,
                  ),
                  routes: [
                    GoRoute(
                      path: ('email-verification'),
                      builder: (context, state) => EmailVerification(),
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),
      ],
    ),
    GoRoute(
      path: ('/succeed-sign-up'),
      builder: (context, state) => const SucceedSignUp(),
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
      // 기본 색상
      theme: ThemeData(
        primaryColor: const Color.fromRGBO(51, 51, 51, 1),
        buttonTheme:
            const ButtonThemeData(buttonColor: Color.fromRGBO(51, 51, 51, 1)),
      ),
      routerConfig: _router,
    );
  }
}
