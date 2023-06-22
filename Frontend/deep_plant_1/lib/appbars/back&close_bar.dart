// 뒤로가기& 닫기 버튼이 둘 다 있는 AppBar

import 'package:flutter/material.dart';

class back_close_bar extends StatelessWidget implements PreferredSizeWidget {
  final String title;
  final bool back;
  final bool close;

  const back_close_bar(
      {required this.back, required this.close, required this.title});

  @override
  Widget build(BuildContext context) {
    return AppBar(
      elevation: 0,
      leading: back
          ? IconButton(
              icon: Icon(
                Icons.arrow_back_ios,
                color: Colors.black,
              ),
              onPressed: () {
                // Handle back button pressed
              },
            )
          : null,
      title: Text(
        title,
        style: TextStyle(
          color: Colors.black,
          fontWeight: FontWeight.bold,
        ),
      ),
      actions: close
          ? [
              IconButton(
                icon: Icon(
                  Icons.close,
                  color: Colors.black,
                ),
                onPressed: () {},
              ),
            ]
          : null,
      backgroundColor: Colors.white,
    );
  }

  @override
  Size get preferredSize => Size.fromHeight(kToolbarHeight);
}
