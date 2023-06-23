import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:deep_plant_app/models/user_model.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class InsertionIdnPw extends StatefulWidget {
  final UserModel? user;
  const InsertionIdnPw({
    super.key,
    required this.user,
  });

  @override
  State<InsertionIdnPw> createState() => _InsertionIdnPwState();
}

class _InsertionIdnPwState extends State<InsertionIdnPw> {
  final _formKey = GlobalKey<FormState>(); // form 구성

  List<String> dropdownList = ['사용자 1', '사용자 2', '사용자 3'];
  String selectedDropdown = '사용자 1';
  String userLevel = 'users_1';
  String _userName = '';
  String _userEmail = '';
  final String _userId = '';
  final String _userPw = '';

  // firbase authentic
  final _authentication = FirebaseAuth.instance;

  // 아이디 유효성 검사
  String? idValidate(String? value) {
    if (value!.isEmpty || !value.contains('@') || !value.contains('.')) {
      return '아이디를 확인하세요.';
    }
    return null;
  }

  // 비밀번호 유효성 검사
  String? pwValidate(String? value) {
    if (value!.isEmpty || value.length < 10) {
      return '비밀번호를 확인하세요.';
    }

    return null;
  }

  // 유효성 검사 함수
  void _tryValidation() {
    final isValid = _formKey.currentState!.validate();
    if (isValid) {
      _formKey.currentState!.save();
    }
  }

  Color buttonColor = const Color.fromRGBO(51, 51, 51, 1).withOpacity(0.5);

  TextEditingController textFieldController1 = TextEditingController();
  TextEditingController textFieldController2 = TextEditingController();
  TextEditingController textFieldController3 = TextEditingController();
  TextEditingController textFieldController4 = TextEditingController();

  void checkTextFieldValues() {
    if (textFieldController1.text.isNotEmpty &&
        textFieldController2.text.isNotEmpty &&
        textFieldController3.text.isNotEmpty &&
        textFieldController4.text.isNotEmpty) {
      setState(() {
        buttonColor = Theme.of(context).primaryColor;
      });
    } else {
      setState(() {
        buttonColor = Theme.of(context).primaryColor.withOpacity(0.5);
      });
    }
  }

  void saveUserData() async {
    CollectionReference users =
        FirebaseFirestore.instance.collection(userLevel);

    // 데이터 생성
    Map<String, dynamic> data = {
      'name': widget.user!.name,
      'email': widget.user!.email,
      'isAlarmed': widget.user!.isAlarmed,
    };

    // 데이터 저장
    DocumentReference document = users.doc(widget.user!.email);
    await document.set(data);
  }

  Future<void> getByEmail(String email) async {
    CollectionReference users =
        FirebaseFirestore.instance.collection(userLevel);

    // 이메일에 해당하는 문서 참조
    DocumentReference documentReference = users.doc(email);
    DocumentSnapshot documentSnapshot = await documentReference.get();

    if (documentSnapshot.exists) {
      // 이메일에 해당하는 문서가 있는 경우
      print('Matching Document ID: ${documentSnapshot.id}');
      print('Name: ${documentSnapshot.get('name')}');

      // 추가 작업 수행 가능
    } else {
      // 이메일에 해당하는 문서가 없는 경우
      print('No matching document found.');
    }
  }

  @override
  void dispose() {
    textFieldController1.dispose();
    textFieldController2.dispose();
    textFieldController3.dispose();
    textFieldController4.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
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
      body: GestureDetector(
        onTap: () {
          FocusScope.of(context).unfocus(); // 키보드 unfocus
        },
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Padding(
                padding: const EdgeInsets.all(10.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Padding(
                      padding: EdgeInsets.only(left: 10),
                      child: Text('*이름'),
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Container(
                          // 이름 입력 필드
                          width: 350,
                          margin: const EdgeInsets.symmetric(vertical: 3),
                          child: TextFormField(
                            controller: textFieldController1,
                            // 유효성 검사
                            validator: (value) {
                              if (value!.isEmpty || !value.contains('@')) {
                                return '올바른 아이디를 입력하세요.';
                              }
                              return null;
                            },
                            onSaved: (value) {
                              _userName = value!;
                            },
                            onChanged: (value) {
                              checkTextFieldValues();
                              widget.user!.name = value;
                            },

                            decoration: InputDecoration(
                                label: const Text('이름'),
                                filled: true,
                                fillColor: Colors.grey[200],
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
                    const Padding(
                      padding: EdgeInsets.only(left: 10.0),
                      child: Text('*이메일'),
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Container(
                          // 아이디 입력 필드
                          width: 250,
                          margin: const EdgeInsets.symmetric(vertical: 3),
                          child: TextFormField(
                            controller: textFieldController2,
                            // 유효성 검사
                            validator: (value) {
                              if (value!.isEmpty || !value.contains('@')) {
                                return '올바른 아이디를 입력하세요.';
                              }
                              return null;
                            },
                            onSaved: (value) {
                              _userEmail = value!;
                            },
                            onChanged: (value) {
                              checkTextFieldValues();
                              widget.user!.email = value;
                              _userEmail = value;
                            },

                            decoration: InputDecoration(
                                label: const Text('example@example.com'),
                                filled: true,
                                fillColor: Colors.grey[200],
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
                            onPressed: () async {
                              getByEmail(_userEmail);
                            },
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
                    const Padding(
                      padding: EdgeInsets.only(left: 10.0),
                      child: Text('*비밀번호'),
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Container(
                          // 비밀번호 입력 필드
                          width: 350,
                          margin: const EdgeInsets.symmetric(vertical: 3),
                          child: TextFormField(
                            controller: textFieldController3,
                            // 유효성 검사
                            validator: (value) {
                              if (value!.isEmpty || !value.contains('@')) {
                                return '올바른 아이디를 입력하세요.';
                              }
                              return null;
                            },
                            onSaved: (value) {},
                            onChanged: (value) {
                              checkTextFieldValues();
                            },

                            decoration: InputDecoration(
                                label: const Text('영문+숫자'),
                                filled: true,
                                fillColor: Colors.grey[200],
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
                          // 비밀번호 재입력 필드
                          width: 350,
                          margin: const EdgeInsets.symmetric(vertical: 3),
                          child: TextFormField(
                            controller: textFieldController4,
                            // 유효성 검사
                            validator: (value) {
                              if (value!.isEmpty || !value.contains('@')) {
                                return '올바른 아이디를 입력하세요.';
                              }
                              return null;
                            },
                            onSaved: (value) {},
                            onChanged: (value) {
                              checkTextFieldValues();
                            },

                            decoration: InputDecoration(
                                label: const Text('비밀번호 확인'),
                                filled: true,
                                fillColor: Colors.grey[200],
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
                    const Padding(
                      padding: EdgeInsets.only(left: 10.0),
                      child: Text('권한'),
                    ),
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
                            padding: const EdgeInsets.only(left: 40),
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
                              if (value == dropdownList[0]) {
                                userLevel = 'users_1';
                              } else if (value == dropdownList[1]) {
                                userLevel = 'users_2';
                              } else {
                                userLevel = 'users_3';
                              }
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
                      ],
                    ),
                    const SizedBox(height: 16),
                    const Padding(
                      padding: EdgeInsets.only(left: 10.0),
                      child: Text('소속'),
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
                                label: const Text('회사명 입력'),
                                filled: true,
                                fillColor: Colors.grey[200],
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
                  onPressed: buttonColor == Theme.of(context).primaryColor
                      ? () async {
                          saveUserData();
                          context.go(
                              '/sign-in/certification/insert-id-pw/succeed-sign-up');
                        }
                      : null,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: buttonColor,
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
      ),
    );
  }
}
