//pdf 49페이지

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth_project/buttons/save_button.dart';
import 'package:firebase_auth_project/buttons/toggle.dart';
import 'package:flutter/material.dart';

const List<Widget> Marbling = <Widget>[
  Text('없음'),
  Text('약간\n있음'),
  Text('보통'),
  Text('약간\n많음'),
  Text('많음'),
];

const List<Widget> Color = <Widget>[
  Text('없음'),
  Text('약간\n있음'),
  Text('보통'),
  Text('어두움'),
  Text('어둡고\n진함'),
];

const List<Widget> Texture = <Widget>[
  Text('흐물함'),
  Text('약간\n흐물함'),
  Text('보통'),
  Text('약간\n단단함'),
  Text('단단함'),
];

const List<Widget> SurfaceMoisture = <Widget>[
  Text('없음'),
  Text('약간\n있음'),
  Text('보통'),
  Text('약간\n많음'),
  Text('많음'),
];

const List<Widget> Overall = <Widget>[
  Text('나쁨'),
  Text('약간\n나쁨'),
  Text('보통'),
  Text('약간\n좋음'),
  Text('좋음'),
];

class FreshMeat_Evaluation extends StatefulWidget {
  const FreshMeat_Evaluation({super.key});

  @override
  State<FreshMeat_Evaluation> createState() => _FreshMeat_EvaluationState();
}

class _FreshMeat_EvaluationState extends State<FreshMeat_Evaluation> {
  final List<bool> _selectedMarbling = <bool>[
    false,
    false,
    false,
    false,
    false
  ];
  final List<bool> _selectedColor = <bool>[false, false, false, false, false];
  final List<bool> _selectedTexture = <bool>[false, false, false, false, false];
  final List<bool> _selectedSurfaceMoisture = <bool>[
    false,
    false,
    false,
    false,
    false
  ];
  final List<bool> _selectedOverall = <bool>[false, false, false, false, false];

  void _sendevalution() async {
    int marblingIndex = _selectedMarbling.indexOf(true) + 1;
    int colorIndex = _selectedColor.indexOf(true) + 1;
    int textureIndex = _selectedTexture.indexOf(true) + 1;
    int surfaceMoistureIndex = _selectedSurfaceMoisture.indexOf(true) + 1;
    int overallIndex = _selectedOverall.indexOf(true) + 1;

    FirebaseFirestore.instance
        .collection('evaluation')
        .doc('zFAaDoaPbUC32ApIYqzR')
        .collection('freshmeat')
        .add({
      'Marbling': marblingIndex,
      'Color': colorIndex,
      'Texture': textureIndex,
      'SurfaceMoisture': surfaceMoistureIndex,
      'Overall': overallIndex,
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        leading: IconButton(
          icon: Icon(
            Icons.arrow_back_ios,
            color: Colors.black,
          ),
          onPressed: () {},
        ),
        title: Text(
          '육류 등록',
          style: TextStyle(
            color: Colors.black,
            fontWeight: FontWeight.bold,
          ),
        ),
        actions: [
          IconButton(
            icon: Icon(
              Icons.close,
              color: Colors.black,
            ),
            onPressed: () {},
          ),
        ],
        backgroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 1),
        child: SingleChildScrollView(
          child: Center(
            child: Column(
              children: [
                Icon(
                  Icons.line_axis,
                  size: 50,
                ),
                Text(
                  '신선육관능평가',
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      'Marbling',
                      style: TextStyle(
                        fontSize: 20,
                      ),
                    ),
                    SizedBox(
                      width: 5.0,
                    ),
                    Text('마블링 정도')
                  ],
                ),
                Row(
                  children: [
                    MyToggleButtons(
                      options: Marbling,
                      isSelected: _selectedMarbling,
                    ),
                  ],
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      'Color',
                      style: TextStyle(
                        fontSize: 20,
                      ),
                    ),
                    SizedBox(
                      width: 5.0,
                    ),
                    Text('육색')
                  ],
                ),
                Row(
                  children: [
                    MyToggleButtons(options: Color, isSelected: _selectedColor),
                  ],
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      'Texture',
                      style: TextStyle(
                        fontSize: 20,
                      ),
                    ),
                    SizedBox(
                      width: 5.0,
                    ),
                    Text('조직감')
                  ],
                ),
                Row(
                  children: [
                    MyToggleButtons(
                        options: Texture, isSelected: _selectedTexture)
                  ],
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      'Surface Moisture',
                      style: TextStyle(
                        fontSize: 20,
                      ),
                    ),
                    SizedBox(
                      width: 5.0,
                    ),
                    Text('표면 육즙')
                  ],
                ),
                Row(
                  children: [
                    MyToggleButtons(
                        options: SurfaceMoisture,
                        isSelected: _selectedSurfaceMoisture)
                  ],
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      'Overall',
                      style: TextStyle(
                        fontSize: 20,
                      ),
                    ),
                    SizedBox(
                      width: 5.0,
                    ),
                    Text('종합기호도')
                  ],
                ),
                Row(
                  children: [
                    MyToggleButtons(
                        options: Overall, isSelected: _selectedOverall)
                  ],
                ),
                SizedBox(
                  height: 5,
                ),
                // ElevatedButton(
                //   onPressed: _sendevalution,
                //   style: ElevatedButton.styleFrom(
                //     backgroundColor: Colors.grey[800],
                //     padding:
                //         EdgeInsets.symmetric(horizontal: 150, vertical: 10),
                //     shape: RoundedRectangleBorder(
                //       borderRadius: BorderRadius.circular(8),
                //     ),
                //   ),
                //   child: Text(
                //     '저장',
                //     style: TextStyle(
                //       fontSize: 22,
                //     ),
                //   ),
                // ),
                SaveButton(onPressed: _sendevalution),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
