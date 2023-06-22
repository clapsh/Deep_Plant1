//pdf 76페이지
import 'package:deep_plant_1/appbar/custom_appbar.dart';
import 'package:deep_plant_1/buttons/save_button.dart';
import 'package:deep_plant_1/textfield/field_with_desc.dart';
import 'package:flutter/material.dart';

class tongue extends StatefulWidget {
  const tongue({super.key});

  @override
  State<tongue> createState() => _tongueState();
}

class _tongueState extends State<tongue> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar:
          CustomAppBar(title: '연구데이터', back_button: true, close_button: true),
      body: Column(
        children: [
          Text(
            '전자혀 데이터',
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                children: [
                  FieldRow(firstText: 'Sourness', secondText: '신맛'),
                  FieldRow(firstText: 'Bitterness', secondText: '진한맛'),
                  FieldRow(firstText: 'Umami', secondText: '감칠맛'),
                  FieldRow(firstText: 'Richness', secondText: '후미'),
                ],
              ),
            ),
          ),
          SaveButton(onPressed: () {}),
        ],
      ),
    );
  }
}
