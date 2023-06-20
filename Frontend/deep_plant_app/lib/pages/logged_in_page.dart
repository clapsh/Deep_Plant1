import 'dart:io';

import 'package:deep_plant_app/pages/show_image.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_storage/firebase_storage.dart';
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

  // 이미지 촬영을 위한 메소드이다.
  // ImagePicker()로 해당 메소드를 호출하고,
  // 카메라를 source로 하여 촬영한다.
  void _pickImage() async {
    final imagePicker = ImagePicker();
    final pickedImageFile = await imagePicker.pickImage(
      source: ImageSource.camera,
      imageQuality: 100,
    );

    setState(() {
      isLoading = true;

      if (pickedImageFile != null) {
        // 만약 촬영한 이미지 파일이 존재한다면 해당 코드를 실행한다.
        // pickedImage에 촬영한 이미지를 달아놓는다.
        pickedImage = File(pickedImageFile.path);
      }
    });
    // Firebase Storage의 저장 위치를 가리키는 변수를 생성하고 putFile()을 통해 촬영한 이미지를 해당 위치에 저장한다.
    final refImage = FirebaseStorage.instance
        .ref()
        .child(loggedUser!.uid)
        .child('${DateTime.now()}.png');
    await refImage.putFile(pickedImage!);
    setState(() {
      isLoading = false;
    });

    turnPage();
  }

  @override
  void initState() {
    super.initState();
    getCurrentUser();
  }

  void turnPage() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ShowImage(image: pickedImage),
      ),
    );
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
            isLoading ? const CircularProgressIndicator() : Container(),
          ],
        ),
      ),
    );
  }
}
