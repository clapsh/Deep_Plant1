import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class InsertionIdnPw extends StatelessWidget {
  const InsertionIdnPw({super.key});

  @override
  Widget build(BuildContext context) {
    List<String> dropdownList = ['사용자 1', '사용자 2', '3'];
    String selectedDropdown = '사용자 1';
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text(
          '아이디/비밀번호',
          style: TextStyle(
            color: Colors.black,
            fontWeight: FontWeight.bold,
          ),
        ),
        elevation: 0,
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Padding(
              padding: const EdgeInsets.all(10.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('*아이디'),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        // 아이디 입력 필드
                        width: 250,
                        margin: const EdgeInsets.symmetric(vertical: 3),
                        child: TextFormField(
                          // 유효성 검사
                          validator: (value) {
                            if (value!.isEmpty || !value.contains('@')) {
                              return '올바른 아이디를 입력하세요.';
                            }
                            return null;
                          },
                          onSaved: (value) {},
                          onChanged: (value) {},

                          decoration: InputDecoration(
                              label: const Text('영문/숫자'),
                              filled: true,
                              fillColor: Colors.grey[200],
                              hintText: '아이디를 입력하세요', // 입력 필드에 힌트로 표시될 텍스트

                              suffixIcon: null, // 입력 필드 오른쪽에 표시될 아이콘
                              border: const OutlineInputBorder(
                                borderRadius: BorderRadius.only(
                                  topLeft: Radius.circular(30),
                                  bottomLeft: Radius.circular(30),
                                ),
                                borderSide: BorderSide.none,
                              ),
                              contentPadding:
                                  const EdgeInsets.symmetric(horizontal: 16)),
                        ),
                      ),
                      SizedBox(
                        width: 100,
                        height: 48,
                        child: ElevatedButton(
                          onPressed: () {},
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Theme.of(context).primaryColor,
                            shape: const RoundedRectangleBorder(
                              borderRadius: BorderRadius.only(
                                topRight: Radius.circular(30),
                                bottomRight: Radius.circular(30),
                              ),
                            ),
                          ),
                          child: const Text(
                            '중복확인',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 18,
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  const Text('*비밀번호'),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        // 아이디 입력 필드
                        width: 350,
                        margin: const EdgeInsets.symmetric(vertical: 3),
                        child: TextFormField(
                          // 유효성 검사
                          validator: (value) {
                            if (value!.isEmpty || !value.contains('@')) {
                              return '올바른 아이디를 입력하세요.';
                            }
                            return null;
                          },
                          onSaved: (value) {},
                          onChanged: (value) {},

                          decoration: InputDecoration(
                              label: const Text('영문+숫자'),
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
                    ],
                  ),
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        // 아이디 입력 필드
                        width: 350,
                        margin: const EdgeInsets.symmetric(vertical: 3),
                        child: TextFormField(
                          // 유효성 검사
                          validator: (value) {
                            if (value!.isEmpty || !value.contains('@')) {
                              return '올바른 아이디를 입력하세요.';
                            }
                            return null;
                          },
                          onSaved: (value) {},
                          onChanged: (value) {},

                          decoration: InputDecoration(
                              label: const Text('비밀번호 확인'),
                              filled: true,
                              fillColor: Colors.grey[200],
                              hintText: '비밀번호 확인', // 입력 필드에 힌트로 표시될 텍스트

                              suffixIcon: null, // 입력 필드 오른쪽에 표시될 아이콘
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(30),
                                borderSide: BorderSide.none,
                              ),
                              contentPadding:
                                  const EdgeInsets.symmetric(horizontal: 16)),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  const Text('권한'),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        // dropdown 버튼
                        width: 350,
                        height: 48,
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
                          onChanged: (dynamic value) {},
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
                    ],
                  ),
                  const SizedBox(height: 16),
                  const Text('소속'),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        // 아이디 입력 필드
                        width: 350,
                        margin: const EdgeInsets.symmetric(vertical: 3),
                        child: TextFormField(
                          // 유효성 검사
                          validator: (value) {
                            if (value!.isEmpty || !value.contains('@')) {
                              return '올바른 아이디를 입력하세요.';
                            }
                            return null;
                          },
                          onSaved: (value) {},
                          onChanged: (value) {},

                          decoration: InputDecoration(
                              label: const Text('회사명 입력'),
                              filled: true,
                              fillColor: Colors.grey[200],
                              hintText: '회사명 입력', // 입력 필드에 힌트로 표시될 텍스트

                              suffixIcon: null, // 입력 필드 오른쪽에 표시될 아이콘
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(30),
                                borderSide: BorderSide.none,
                              ),
                              contentPadding:
                                  const EdgeInsets.symmetric(horizontal: 16)),
                        ),
                      ),
                    ],
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        // 아이디 입력 필드
                        width: 350,
                        margin: const EdgeInsets.symmetric(vertical: 3),
                        child: TextFormField(
                          // 유효성 검사
                          validator: (value) {
                            if (value!.isEmpty || !value.contains('@')) {
                              return '올바른 아이디를 입력하세요.';
                            }
                            return null;
                          },
                          onSaved: (value) {},
                          onChanged: (value) {},

                          decoration: InputDecoration(
                              label: const Text('직책 입력'),
                              filled: true,
                              fillColor: Colors.grey[200],
                              hintText: '비밀번호 확인', // 입력 필드에 힌트로 표시될 텍스트

                              suffixIcon: null, // 입력 필드 오른쪽에 표시될 아이콘
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(30),
                                borderSide: BorderSide.none,
                              ),
                              contentPadding:
                                  const EdgeInsets.symmetric(horizontal: 16)),
                        ),
                      ),
                    ],
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        // 아이디 입력 필드
                        width: 250,
                        margin: const EdgeInsets.symmetric(vertical: 3),
                        child: TextFormField(
                          // 유효성 검사
                          validator: (value) {
                            if (value!.isEmpty || !value.contains('@')) {
                              return '올바른 아이디를 입력하세요.';
                            }
                            return null;
                          },
                          onSaved: (value) {},
                          onChanged: (value) {},

                          decoration: InputDecoration(
                              label: const Text('회사주소 검색'),
                              filled: true,
                              fillColor: Colors.grey[200],
                              hintText: '아이디를 입력하세요', // 입력 필드에 힌트로 표시될 텍스트

                              suffixIcon: null, // 입력 필드 오른쪽에 표시될 아이콘
                              border: const OutlineInputBorder(
                                borderRadius: BorderRadius.only(
                                  topLeft: Radius.circular(30),
                                  bottomLeft: Radius.circular(30),
                                ),
                                borderSide: BorderSide.none,
                              ),
                              contentPadding:
                                  const EdgeInsets.symmetric(horizontal: 16)),
                        ),
                      ),
                      SizedBox(
                        width: 100,
                        height: 48,
                        child: ElevatedButton(
                          onPressed: () {},
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Theme.of(context).primaryColor,
                            shape: const RoundedRectangleBorder(
                              borderRadius: BorderRadius.only(
                                topRight: Radius.circular(30),
                                bottomRight: Radius.circular(30),
                              ),
                            ),
                          ),
                          child: const Text(
                            '검색',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 18,
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            SizedBox(
              width: 350,
              height: 50,
              child: ElevatedButton(
                onPressed: () {
                  context.go(
                      '/sign-in/certification/insert-id-pw/succeed-sign-up');
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Theme.of(context).primaryColor,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
                child: const Text(
                  '다음',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
