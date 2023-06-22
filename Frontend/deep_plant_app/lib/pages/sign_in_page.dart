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

  // 유효성 확인 함수
  void _tryValidation() {
    final isValid = _formKey.currentState!.validate();
    if (isValid) {
      _formKey.currentState!.save();
    }
  }

  // 데이터를 가져오는 비동기 함수
  void fetchData() async {
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

    // 데이터 fetch 성공시 다음 페이지를 push
    Future.delayed(Duration.zero, () {
      currentContext.pushReplacement('/option');
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
          FocusScope.of(context).unfocus(); // 키보드 unfocus
        },
        child: Center(
          child: SingleChildScrollView(
            child: Form(
              key: _formKey,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Padding(
                    // 딥플랜트 로고 이미지
                    padding: const EdgeInsets.only(bottom: 20),
                    child: ColorFiltered(
                      colorFilter: const ColorFilter.mode(
                          Colors.black, BlendMode.modulate),
                      child: Image.asset(
                        'assets/images/logo.png',
                        width: 300,
                        height: 60,
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
                    // 아이디 입력 필드
                    padding: const EdgeInsets.fromLTRB(60, 5, 60, 10),
                    child: TextFormField(
                      // 유효성 검사
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
                    // 비밀번호 입력 필드
                    padding: const EdgeInsets.fromLTRB(60, 0, 60, 10),
                    child: TextFormField(
                      obscureText: true,
                      // 유효성 검사
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
                      // 로그인 버튼
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
                      // 데이터를 처리하는 동안 로딩 위젯 보여주기
                      isLoading
                          ? const CircularProgressIndicator()
                          : Container(),
                    ],
                  ),
                  // 비밀번호 찾기 버튼
                  TextButton(
                    onPressed: () {},
                    child: const Text(
                      '비밀번호 찾기',
                      style: TextStyle(
                        color: Colors.black54,
                      ),
                    ),
                  ),
                  // 회원가입 버튼
                  SizedBox(
                    width: 150,
                    child: ElevatedButton(
                      onPressed: () {
                        // 회원가입 페이지를 push
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
