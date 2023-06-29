import 'package:flutter/material.dart';

class CustomAppBar extends StatelessWidget implements PreferredSizeWidget {
  final String title;
  final bool back_button;
  final bool close_button;
  final VoidCallback? backButtonOnPressed;
  final VoidCallback? closeButtonOnPressed;

  const CustomAppBar({
    required this.title,
    required this.back_button,
    required this.close_button,
    this.backButtonOnPressed,
    this.closeButtonOnPressed,
  });

  @override
  Widget build(BuildContext context) {
    return AppBar(
      elevation: 0,
      leading: back_button
          ? IconButton(
              icon: Icon(
                Icons.arrow_back_ios,
                color: Colors.black,
              ),
              onPressed: backButtonOnPressed != null
                  ? backButtonOnPressed
                  : () {
                      Navigator.pop(context);
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
      actions: close_button
          ? [
              IconButton(
                icon: Icon(
                  Icons.close,
                  color: Colors.black,
                ),
                onPressed: closeButtonOnPressed != null
                    ? closeButtonOnPressed
                    : () {
                        Navigator.pop(context);
                      },
              ),
            ]
          : null,
      backgroundColor: Colors.white,
    );
  }

  @override
  Size get preferredSize => Size.fromHeight(kToolbarHeight);
}
