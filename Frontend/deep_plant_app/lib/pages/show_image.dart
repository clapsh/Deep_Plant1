import 'dart:io';

import 'package:deep_plant_app/pages/result_page.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:flutter/material.dart';

class ShowImage extends StatefulWidget {
  final File? image;

  const ShowImage({
    super.key,
    required this.image,
  });

  @override
  State<ShowImage> createState() => _ShowImageState();
}

class _ShowImageState extends State<ShowImage> {
  final _authentication = FirebaseAuth.instance;
  User? loggedUser;
  bool _isLoading = false;

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

  // 이미지를 firebase storage에 저장하는 비동기 함수
  void saveImage() async {
    setState(() {
      _isLoading = true;
    });
    try {
      // 이미지를 firbaseStorage에 userid/시간.png 형식으로 저장
      final refImage = FirebaseStorage.instance
          .ref()
          .child(loggedUser!.uid)
          .child('${DateTime.now()}.png');
      await refImage.putFile(widget.image!);
    } catch (e) {
      print(e);
      setState(() {
        _isLoading = false;
      });
    }

    setState(() {
      _isLoading = false;
    });
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
        title: const Text('촬영한 사진'),
        backgroundColor: Theme.of(context).primaryColor,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // 촬영한 이미지 보여주는 위젯
            Container(
              width: 350,
              height: 500,
              decoration: BoxDecoration(
                image: widget.image != null
                    ? DecorationImage(
                        image: FileImage(widget.image!),
                        fit: BoxFit.cover,
                      )
                    : null,
              ),
            ),
            _isLoading
                ? const CircularProgressIndicator()
                : const SizedBox(
                    height: 15,
                  ),
            SizedBox(
              width: 150,
              // 분석하기 버튼
              // 분석하기 버튼을 누르면 이미지가 촬영한 이미지가 firebase로 저장된다.
              child: ElevatedButton(
                onPressed: () async {
                  saveImage();

                  // 이미지 저장하고 다음 페이지 push
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => const ResultPage(),
                    ),
                  );
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Theme.of(context).primaryColor,
                ),
                child: const Text(
                  '분석하기',
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
    );
  }
}
