import 'dart:io';

import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:deep_plant_app/source/widgets.dart';

class LoggedInPage extends StatefulWidget {
  const LoggedInPage({
    super.key,
    this.image,
  });

  final File? image;

  @override
  State<LoggedInPage> createState() => _LoggedInPageState();
}

class _LoggedInPageState extends State<LoggedInPage> {
  final _authentication = FirebaseAuth.instance;
  User? loggedUser;
  File? pickedImage;
  bool isLoading = false;
  bool isFinal = false;

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
  }

  // 이미지를 firebase storage에 저장하는 비동기 함수
  Future<void> saveImage() async {
    setState(() {
      isLoading = true;
    });
    try {
      // 이미지를 firbaseStorage에 userid/시간.png 형식으로 저장
      final refImage = FirebaseStorage.instance.ref().child('${loggedUser!.uid}.png');
      await refImage.putFile(widget.image!);
    } catch (e) {
      print(e);
      setState(() {
        isLoading = false;
      });
    }

    setState(() {
      isLoading = false;
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
        title: Padding(
          padding: const EdgeInsets.only(right: 20.0),
          child: Text(
            '육류등록',
            style: TextStyle(fontWeight: FontWeight.bold),
          ),
        ),
        backgroundColor: Colors.white,
        elevation: 0.0,
        foregroundColor: Colors.black,
        actions: [
          elevated(
            colorb: Colors.white,
            colori: Colors.black,
            icon: Icons.close,
          ),
        ],
      ),
      body: Column(
        children: [
          SizedBox(height: 45.0),
          Row(
            children: [
              SizedBox(
                width: (MediaQuery.of(context).size.width) * 0.39,
              ),
              Text(
                '사진등록',
                style: TextStyle(
                  fontSize: 23.0,
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(
                width: (MediaQuery.of(context).size.width) * 0.22,
              ),
              IconButton(
                onPressed: () {},
                icon: Icon(
                  Icons.info_outline,
                  color: Colors.grey[600],
                  size: 30.0,
                ),
              )
            ],
          ),
          Row(
            children: [
              SizedBox(
                width: 30.0,
              ),
              Text(
                '촬영날짜',
                style: TextStyle(
                  color: Colors.grey[600],
                ),
              )
            ],
          ),
          SizedBox(
            height: 10.0,
          ),
          Padding(
            padding: const EdgeInsets.only(left: 25.0, right: 25.0),
            child: Row(
              children: [
                Expanded(
                  flex: 1,
                  child: Container(
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(10.0),
                      color: Colors.grey[400],
                      border: Border.all(
                        color: Colors.grey,
                        width: 0.5,
                      ),
                    ),
                    height: 40.0,
                    child: Text(
                      '월',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 20.0,
                      ),
                    ),
                  ),
                ),
                SizedBox(
                  width: 10.0,
                ),
                Expanded(
                  flex: 1,
                  child: Container(
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(10.0),
                      color: Colors.grey[400],
                      border: Border.all(
                        color: Colors.grey,
                        width: 0.5,
                      ),
                    ),
                    height: 40.0,
                    child: Text(
                      '일',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 20.0,
                      ),
                    ),
                  ),
                ),
                SizedBox(
                  width: 10.0,
                ),
                Expanded(
                  flex: 2,
                  child: Container(
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(10.0),
                      color: Colors.grey[400],
                      border: Border.all(
                        color: Colors.grey,
                        width: 0.5,
                      ),
                    ),
                    height: 40.0,
                    child: Text(
                      '년도',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 20.0,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
          SizedBox(
            height: 10.0,
          ),
          Row(
            children: [
              SizedBox(
                width: 30.0,
              ),
              Text(
                '촬영자',
                style: TextStyle(
                  color: Colors.grey[600],
                ),
              ),
              SizedBox(
                width: 15.0,
              ),
              SizedBox(
                width: 6.0,
                child: Divider(
                  color: Colors.black,
                  thickness: 1.5,
                ),
              ),
            ],
          ),
          SizedBox(
            height: 10.0,
          ),
          Container(
            width: 350,
            height: 400,
            decoration: BoxDecoration(
              color: Colors.white,
              image: pickedImage != null
                  ? DecorationImage(
                      image: FileImage(pickedImage!),
                      fit: BoxFit.cover,
                    )
                  : null,
            ),
            child: pickedImage == null
                ? ElevatedButton(
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
                  )
                : null,
          ),
          // 데이터를 처리하는 동안 로딩 위젯 보여주기
          isLoading ? const CircularProgressIndicator() : Container(),
          Padding(
            padding: const EdgeInsets.all(20.0),
            child: SizedBox(
              height: 55,
              width: 350,
              child: ElevatedButton(
                onPressed: pickedImage != null
                    ? () async {
                        //await saveImage();
                      }
                    : null,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.grey[800],
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10.0),
                  ),
                ),
                child: Text('다음'),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
