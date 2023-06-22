import 'package:deep_plant_1/appbar/custom_appbar.dart';
import 'package:deep_plant_1/buttons/save_button.dart';
import 'package:deep_plant_1/textfield/field_with_desc.dart';
import 'package:flutter/material.dart';

class experiment_data extends StatefulWidget {
  const experiment_data({super.key});

  @override
  State<experiment_data> createState() => _experiment_dataState();
}

class _experiment_dataState extends State<experiment_data> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar:
          CustomAppBar(title: '연구데이터', back_button: true, close_button: true),
      body: Column(
        children: [
          Text(
            '실험데이터',
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: SingleChildScrollView(
                child: Column(
                  children: [
                    FieldRow(firstText: 'DL육즙감량', secondText: ''),
                    FieldRow(firstText: 'CL가열감량', secondText: ''),
                    FieldRow(firstText: 'PH', secondText: ''),
                    FieldRow(firstText: 'WBSF전단가', secondText: ''),
                    FieldRow(firstText: '카텝신활성도', secondText: ''),
                    FieldRow(firstText: 'MFI근소편화지수', secondText: ''),
                  ],
                ),
              ),
            ),
          ),
          SaveButton(onPressed: () {}),
        ],
      ),
    );
  }
}
