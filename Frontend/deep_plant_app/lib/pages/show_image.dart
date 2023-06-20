import 'dart:io';

import 'package:flutter/material.dart';

class ShowImage extends StatelessWidget {
  final File? image;

  const ShowImage({
    super.key,
    required this.image,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('촬영한 사진'),
        backgroundColor: Theme.of(context).primaryColor,
      ),
      body: Center(
        child: Container(
          width: 300,
          height: 300,
          decoration: BoxDecoration(
            image: image != null
                ? DecorationImage(
                    image: FileImage(image!),
                    fit: BoxFit.cover,
                  )
                : null,
          ),
        ),
      ),
    );
  }
}
