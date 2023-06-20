import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class SignIn extends StatefulWidget {
  const SignIn({super.key});

  @override
  State<SignIn> createState() => _SignInState();
}

class _SignInState extends State<SignIn> {
  final _formKey = GlobalKey<FormState>(); // form 구성
  String userId = '';
  String userPw = '';
  bool isLoading = false;

  // firbase authentic
  final _authentication = FirebaseAuth.instance;

  // 유효성 확인
  void _tryValidation() {
    final isValid = _formKey.currentState!.validate();
    if (isValid) {
      _formKey.currentState!.save();
    }
  }

  void fetchData() async {
    // 데이터를 가져오는 비동기 함수
    setState(() {
      isLoading = true; // 로딩 상태를 활성화
    });

    // 데이터를 가져오는 비동기 작업
    try {
      await _authentication.signInWithEmailAndPassword(
        email: userId,
        password: userPw,
      );
    } catch (e) {
      setState(() {
        isLoading = false; // 로딩 상태를 비활성화
      });
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('아이디와 비밀번호를 확인하세요'),
          backgroundColor: Colors.amber,
        ),
      );
      return;
    }

    setState(() {
      isLoading = false; // 로딩 상태를 비활성화
    });

    final currentContext = context;

    Future.delayed(Duration.zero, () {
      currentContext.pushReplacement('/logged-in');
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('로그인'),
        backgroundColor: Theme.of(context).primaryColor,
      ),
      body: GestureDetector(
        onTap: () {
          FocusScope.of(context).unfocus();
        },
        child: Center(
          child: SingleChildScrollView(
            child: Form(
              key: _formKey,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Padding(
                    padding: const EdgeInsets.only(bottom: 20),
                    child: ColorFiltered(
                      colorFilter: const ColorFilter.mode(
                          Colors.black, BlendMode.modulate),
                      child: Image.asset(
                        'assets/images/logo.png',
                        width: 300, // 이미지의 가로 크기 조절
                        height: 60, // 이미지의 세로 크기 조절
                      ),
                    ),
                  ),
                  const Text(
                    '로그인',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.fromLTRB(60, 5, 60, 10),
                    child: TextFormField(
                      validator: (value) {
                        if (value!.isEmpty || !value.contains('@')) {
                          return '올바른 아이디를 입력하세요.';
                        }
                        return null;
                      },
                      onSaved: (value) {
                        userId = value!;
                      },
                      onChanged: (value) {
                        userId = value;
                      },
                      decoration: InputDecoration(
                          filled: true,
                          fillColor: Colors.grey[200],
                          labelText: 'ID', // 입력 필드 위에 표시될 라벨 텍스트
                          hintText: '아이디를 입력하세요', // 입력 필드에 힌트로 표시될 텍스트
                          prefixIcon:
                              const Icon(Icons.person), // 입력 필드 왼쪽에 표시될 아이콘
                          suffixIcon:
                              const Icon(Icons.clear), // 입력 필드 오른쪽에 표시될 아이콘
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(5),
                            borderSide: BorderSide.none,
                          ),
                          contentPadding:
                              const EdgeInsets.symmetric(horizontal: 16)),
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.fromLTRB(60, 0, 60, 10),
                    child: TextFormField(
                      obscureText: true,
                      validator: (value) {
                        if (value!.isEmpty || value.length < 6) {
                          return '올바른 비밀번호를 입력하세요.';
                        }
                        return null;
                      },
                      onSaved: (value) {
                        userPw = value!;
                      },
                      onChanged: (value) {
                        userPw = value;
                      },
                      decoration: InputDecoration(
                          filled: true,
                          fillColor: Colors.grey[200],
                          labelText: 'PW', // 입력 필드 위에 표시될 라벨 텍스트
                          hintText: '비빌번호를 입력하세요', // 입력 필드에 힌트로 표시될 텍스트
                          prefixIcon:
                              const Icon(Icons.key), // 입력 필드 왼쪽에 표시될 아이콘
                          suffixIcon:
                              const Icon(Icons.clear), // 입력 필드 오른쪽에 표시될 아이콘
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(5),
                            borderSide: BorderSide.none,
                          ),
                          contentPadding:
                              const EdgeInsets.symmetric(horizontal: 16)),
                    ),
                  ),
                  Column(
                    children: [
                      SizedBox(
                        width: 290,
                        child: ElevatedButton(
                          onPressed: () async {
                            _tryValidation();
                            fetchData();
                          },
                          style: ElevatedButton.styleFrom(
                            elevation: 3,
                            backgroundColor: Colors.white,
                          ),
                          child: Text(
                            '로그인',
                            style: TextStyle(
                              color: Theme.of(context).primaryColor,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ),
                      isLoading
                          ? const CircularProgressIndicator()
                          : Container(),
                    ],
                  ),
                  TextButton(
                    onPressed: () {},
                    child: const Text(
                      '비밀번호 찾기',
                      style: TextStyle(
                        color: Colors.black54,
                      ),
                    ),
                  ),
                  SizedBox(
                    width: 150,
                    child: ElevatedButton(
                      onPressed: () {
                        context.go('/sign-in/sign-up');
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Theme.of(context).primaryColor,
                      ),
                      child: const Text(
                        '회원가입',
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
