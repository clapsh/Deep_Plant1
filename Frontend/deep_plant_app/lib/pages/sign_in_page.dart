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
  bool isChecked = false;

  // dropdown 버튼 리스트
  List<String> dropdownList = ['사용자 1', '사용자 2', '3'];
  String selectedDropdown = '사용자 1';

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
      currentContext.pushReplacement('/logged-in');
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
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
                    padding: const EdgeInsets.only(bottom: 5),
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
                    '딥에이징',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(
                    height: 60,
                  ),
                  Container(
                    // 아이디 입력 필드
                    padding: const EdgeInsets.symmetric(horizontal: 55),
                    margin: const EdgeInsets.symmetric(vertical: 3),
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
                          label: const Center(
                            child: Text('아이디'),
                          ),
                          filled: true,
                          fillColor: Colors.grey[200],
                          hintText: '아이디를 입력하세요', // 입력 필드에 힌트로 표시될 텍스트

                          suffixIcon: null, // 입력 필드 오른쪽에 표시될 아이콘
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(30),
                            borderSide: BorderSide.none,
                          ),
                          contentPadding:
                              const EdgeInsets.symmetric(horizontal: 16)),
                    ),
                  ),
                  Container(
                    // 비밀번호 입력 필드
                    padding: const EdgeInsets.symmetric(horizontal: 55),
                    margin: const EdgeInsets.symmetric(vertical: 3),
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
                          label: const Center(
                            child: Text('비밀번호'),
                          ),
                          filled: true,
                          fillColor: Colors.grey[200],
                          hintText: '비빌번호를 입력하세요', // 입력 필드에 힌트로 표시될 텍스트
                          suffixIcon: null, // 입력 필드 오른쪽에 표시될 아이콘
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(30),
                            borderSide: BorderSide.none,
                          ),
                          contentPadding:
                              const EdgeInsets.symmetric(horizontal: 16)),
                    ),
                  ),
                  Container(
                    // dropdown 버튼
                    width: 300,
                    height: 50,
                    margin: const EdgeInsets.symmetric(vertical: 3),

                    decoration: BoxDecoration(
                        border: Border.all(
                          color: Colors.grey.shade400,
                          width: 1.0,
                        ),
                        borderRadius: BorderRadius.circular(30)),
                    child: DropdownButton(
                      value: selectedDropdown,
                      items: dropdownList.map((String item) {
                        return DropdownMenuItem<String>(
                          value: item,
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Center(
                                child: Text(
                                  item,
                                ),
                              ),
                            ],
                          ),
                        );
                      }).toList(),
                      onChanged: (dynamic value) {
                        setState(() {
                          selectedDropdown = value;
                        });
                      },
                      isExpanded: true,
                      borderRadius: BorderRadius.circular(30),
                      underline: Container(
                        decoration: const BoxDecoration(
                          border: Border(
                              bottom: BorderSide(
                                  color: Colors.transparent, width: 0)),
                        ),
                      ),
                      icon: const Icon(
                        Icons.arrow_drop_down_sharp,
                        size: 40,
                      ),
                    ),
                  ),

                  // 회원가입 버튼
                  TextButton(
                    onPressed: () {
                      // 회원가입 페이지를 push
                      context.go('/sign-in/certification');
                    },
                    child: const Text(
                      '회원가입',
                      style: TextStyle(
                        color: Colors.black54,
                      ),
                    ),
                  ),
                  Row(
                    children: [
                      const SizedBox(
                        width: 40,
                      ),
                      Checkbox(
                        value: isChecked,
                        onChanged: (value) {},
                      ),
                      const Text('자동 로그인'),
                    ],
                  ),
                  const SizedBox(
                    height: 45,
                  ),
                  SizedBox(
                    width: 200,
                    height: 50,
                    child: ElevatedButton(
                      onPressed: () async {
                        _tryValidation();
                        fetchData();
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Theme.of(context).primaryColor,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(30),
                        ),
                      ),
                      child: const Text(
                        '확인',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 18,
                        ),
                      ),
                    ),
                  ),
                  // 데이터를 처리하는 동안 로딩 위젯 보여주기
                  isLoading ? const CircularProgressIndicator() : Container(),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
