import 'package:flutter/material.dart';

class FieldRow extends StatelessWidget {
  late final String firstText;
  late final String secondText;
  FieldRow({required this.firstText, required this.secondText});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.fromLTRB(30, 0, 30, 0),
      child: Row(
        children: [
          SizedBox(height: 100),
          Text(
            firstText,
            style: TextStyle(
              fontSize: 20,
            ),
          ),
          SizedBox(
            width: 10,
          ),
          Text(secondText),
          Expanded(
            child: Align(
              alignment: Alignment.centerRight,
              child: SizedBox(
                width: 160,
                child: TextField(
                  decoration: InputDecoration(
                    labelText: firstText,
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
