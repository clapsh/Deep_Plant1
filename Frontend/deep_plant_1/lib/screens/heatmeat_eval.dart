//pdf 75페이지

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth_project/buttons/save_button.dart';
import 'package:firebase_auth_project/buttons/toggle.dart';
import 'package:flutter/material.dart';

const List<Widget> Flavor = <Widget>[
  Text('약간'), //'있음'이 맞는 표현같음. figma 오타인듯?
  Text('약간\n있음'),
  Text('보통'),
  Text('약간\n풍부함'),
  Text('풍부함'),
];

const List<Widget> Juiciness = <Widget>[
  Text('퍽퍽함'),
  Text('약간\n퍽퍽함'),
  Text('보통'),
  Text('약간\n다즙함'),
  Text('다즙함'),
];

const List<Widget> Tenderness = <Widget>[
  Text('질김'),
  Text('약간\n질김'),
  Text('보통'),
  Text('약간\n연함'),
  Text('연함'),
];
const List<Widget> Umami = <Widget>[
  Text('약함'),
  Text('약간\n약함'),
  Text('보통'),
  Text('약간\n좋음'),
  Text('좋음'),
];

const List<Widget> Palatability = <Widget>[
  Text('나쁨'),
  Text('약간\n나쁨'),
  Text('보통'),
  Text('약간\n좋음'),
  Text('좋음'),
];

class HeatMeat_Evaluation extends StatefulWidget {
  const HeatMeat_Evaluation({super.key});

  @override
  State<HeatMeat_Evaluation> createState() => _HeatMeat_EvaluationState();
}

class _HeatMeat_EvaluationState extends State<HeatMeat_Evaluation> {
  final List<bool> _selectedFlavor = <bool>[false, false, false, false, false];
  final List<bool> _selectedJuiciness = <bool>[
    false,
    false,
    false,
    false,
    false
  ];
  final List<bool> _selectedTenderness = <bool>[
    false,
    false,
    false,
    false,
    false
  ];
  final List<bool> _selectedUmami = <bool>[false, false, false, false, false];
  final List<bool> _selectedPalatability = <bool>[
    false,
    false,
    false,
    false,
    false
  ];

  void _sendevalution() async {
    int FlavorIndex = _selectedFlavor.indexOf(true) + 1;
    int JuicinessIndex = _selectedJuiciness.indexOf(true) + 1;
    int TendernessIndex = _selectedTenderness.indexOf(true) + 1;
    int UmamiIndex = _selectedUmami.indexOf(true) + 1;
    int PalatabilityIndex = _selectedPalatability.indexOf(true) + 1;

    FirebaseFirestore.instance
        .collection('evaluation')
        .doc('zFAaDoaPbUC32ApIYqzR')
        .collection('heatmeat')
        .add({
      'Flavor': FlavorIndex,
      'Juiciness': JuicinessIndex,
      'Tenderness': TendernessIndex,
      'Umami': UmamiIndex,
      'Palatability': PalatabilityIndex,
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
        padding: const EdgeInsets.symmetric(horizontal: 30),
        child: Expanded(
          child: SingleChildScrollView(
            child: Column(
              children: [
                Text(
                  '가열육 관능평가 데이터',
                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                SizedBox(
                  height: 20,
                ),
                Row(
                  children: [
                    Text(
                      'Flavor',
                      style: TextStyle(
                        fontSize: 22,
                      ),
                    ),
                    SizedBox(
                      width: 5.0,
                    ),
                    Text('풍미')
                  ],
                ),
                MyToggleButtons(
                  options: Flavor,
                  isSelected: _selectedFlavor,
                ),
                Row(
                  children: [
                    Text(
                      'Juiciness',
                      style: TextStyle(
                        fontSize: 22,
                      ),
                    ),
                    SizedBox(
                      width: 5.0,
                    ),
                    Text('다즙성')
                  ],
                ),
                MyToggleButtons(
                    options: Juiciness, isSelected: _selectedJuiciness),
                Row(
                  children: [
                    Text(
                      'Tenderness',
                      style: TextStyle(
                        fontSize: 22,
                      ),
                    ),
                    SizedBox(
                      width: 5.0,
                    ),
                    Text('연도')
                  ],
                ),
                MyToggleButtons(
                    options: Tenderness, isSelected: _selectedTenderness),
                Row(
                  children: [
                    Text(
                      'Umami',
                      style: TextStyle(
                        fontSize: 22,
                      ),
                    ),
                    SizedBox(
                      width: 5.0,
                    ),
                    Text('감칠맛')
                  ],
                ),
                MyToggleButtons(options: Umami, isSelected: _selectedUmami),
                Row(
                  children: [
                    Text(
                      'Palatability',
                      style: TextStyle(
                        fontSize: 22,
                      ),
                    ),
                    SizedBox(
                      width: 5.0,
                    ),
                    Text('기호도')
                  ],
                ),
                MyToggleButtons(
                    options: Palatability, isSelected: _selectedPalatability),
                SizedBox(
                  height: 40,
                ),
                SaveButton(onPressed: _sendevalution),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
