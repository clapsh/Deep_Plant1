import 'dart:io';

import 'package:deep_plant_app/pages/show_image.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

class LoggedInPage extends StatefulWidget {
  const LoggedInPage({super.key});

  @override
  State<LoggedInPage> createState() => _LoggedInPageState();
}

class _LoggedInPageState extends State<LoggedInPage> {
  final _authentication = FirebaseAuth.instance;
  User? loggedUser;
  File? pickedImage;
  bool isLoading = false;

  // user 정보 가져오기
  void getCurrentUser() {
    try {
      final user = _authentication.currentUser;
      if (user != null) {
        loggedUser = user;
      }
    } catch (e) {
      print(e);
    }
  }

  // 이미지 촬영을 위한 메소드
  void _pickImage() async {
    final imagePicker = ImagePicker();
    final pickedImageFile = await imagePicker.pickImage(
      source: ImageSource.camera,
      imageQuality: 100,
    );

    setState(() {
      isLoading = true; // 로딩 활성화

      if (pickedImageFile != null) {
        // pickedImage에 촬영한 이미지를 달아놓는다.
        pickedImage = File(pickedImageFile.path);
      }
    });

    setState(() {
      isLoading = false; // 로딩 비활성화
    });

    turnPage(); // 데이터 처리가 완료되면 다음 페이지 push
  }

  // 다음 페이지 push 함수
  void turnPage() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ShowImage(image: pickedImage),
      ),
    );
  }

  @override
  void initState() {
    super.initState();
    getCurrentUser();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        automaticallyImplyLeading: false, // 돌아가기 버튼 제거
        backgroundColor: Theme.of(context).primaryColor,
        title: const Text('Login Succeed!'),
        actions: [
          IconButton(
            onPressed: () {
              _authentication.signOut();
              Navigator.pop(context);
            },
            icon: const Icon(
              Icons.exit_to_app,
              color: Colors.white,
            ),
          ),
        ],
      ),
      body: Center(
        // 카메라 버튼
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SizedBox(
              height: 50,
              child: ElevatedButton(
                onPressed: () {
                  _pickImage();
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Theme.of(context).primaryColor,
                ),
                child: const Icon(
                  Icons.camera_alt,
                  size: 30,
                ),
              ),
            ),
            // 데이터를 처리하는 동안 로딩 위젯 보여주기
            isLoading ? const CircularProgressIndicator() : Container(),
          ],
        ),
      ),
    );
  }
}
