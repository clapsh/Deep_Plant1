import 'package:flutter/material.dart';

class addiTion extends StatefulWidget {
  const addiTion({super.key});

  @override
  State<addiTion> createState() => _addiTionState();
}

class _addiTionState extends State<addiTion> {
  final orders = ['소', '돼지'];
  final largeOrders_1 = ['안심', '등심', '채끝', '목심', '앞다리', '우둔', '설도', '양지', '사태', '갈비'];

  final List<List<String>> tableData = [
    ['안심살'],
    ['윗등심살', '꽃등심살', '아래등심살', '살치살'],
    ['채끝살'],
    ['목심살'],
    ['꾸리살', '부채살', '앞다리살', '갈비덧살', '부채덮개살'],
    ['우둔살', '홍두깨살', '보섭살', '설깃살', '설깃머리살', '도가니살', '삼각살'],
    ['안심살'],
    ['양지머리', '차돌박이', '업진살', '업진안살', '치마양지', '치마살', '앞치마살'],
    ['앞사태', '뒷사태', '뭉치사태', '아롱사태', '상박살'],
    ['본갈비', '꽃갈비', '참갈비', '갈빗살', '마구리', '토시살', '안창살', '제비추리'],
  ];

  String? selectedOrders;
  int selectedorder = 0;
  bool isselectedorder = false;

  String? selectedLarges;
  int selectedlarge = 0;
  bool isselectedlarge = false;

  String? selectedLittles;
  int selectedlittle = 0;

  bool isFinal = false;

  void setOrder(String order) {
    if (order == '돼지') {
      selectedorder = 1;
    }
  }

  void setLarge(String large) {
    for (int i = 0; i < 10; i++) {
      if (large == largeOrders_1[i]) {
        selectedlarge = i;
        break;
      }
    }
  }

  void setLittle(String little) {
    for (int i = 0; i < tableData[selectedlarge].length; i++) {
      if (little == tableData[selectedlarge][i]) {
        selectedlittle = i;
        break;
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
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
        leading: ElevatedButton(
          onPressed: () {},
          child: Icon(
            Icons.arrow_back_ios,
            color: Colors.black,
          ),
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.white,
            elevation: 0.0,
          ),
        ),
        actions: [
          ElevatedButton(
              onPressed: () {},
              child: Icon(
                Icons.close,
                color: Colors.black,
              ),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.white,
                elevation: 0.0,
              )),
        ],
      ),
      body: GestureDetector(
        onTap: () => FocusScope.of(context).unfocus(),
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            children: [
              SizedBox(height: 45.0),
              Align(
                alignment: Alignment.center,
                child: Text(
                  '관리번호 생성을 위한',
                  style: TextStyle(
                    fontSize: 20.0,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              Align(
                alignment: Alignment.center,
                child: Text(
                  '추가 정보를 입력해주세요',
                  style: TextStyle(
                    fontSize: 20.0,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              SizedBox(
                height: 60.0,
              ),
              Padding(
                padding: const EdgeInsets.only(left: 35.0),
                child: Row(
                  children: [
                    Text(
                      '종류',
                      textAlign: TextAlign.start,
                      style: TextStyle(
                        fontSize: 20.0,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
              SizedBox(
                height: 20.0,
              ),
              Container(
                margin: EdgeInsets.only(left: 30.0, right: 30.0),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(25.0),
                  border: Border.all(
                    color: Colors.grey,
                    width: 1.0,
                  ),
                ),
                child: Padding(
                  padding: EdgeInsets.only(left: 15.0, right: 15.0),
                  child: DropdownButton(
                    padding: EdgeInsets.only(left: 25.0),
                    underline: Container(),
                    alignment: Alignment.center,
                    elevation: 1,
                    borderRadius: BorderRadius.circular(25.0),
                    dropdownColor: Colors.grey[100],
                    iconSize: 25.0,
                    isExpanded: true,
                    hint: Text('종류 선택'),
                    iconEnabledColor: Colors.grey[400],
                    value: selectedOrders,
                    items: orders
                        .map((e) => DropdownMenuItem(
                              child: Center(child: Text(e)),
                              value: e,
                            ))
                        .toList(),
                    onChanged: (value) {
                      setState(() {
                        selectedOrders = value!;
                        isselectedorder = true;
                        setOrder(selectedOrders!);
                      });
                    },
                  ),
                ),
              ),
              SizedBox(
                height: 20.0,
              ),
              Padding(
                padding: const EdgeInsets.only(left: 35.0),
                child: Row(
                  children: [
                    Text(
                      '부위',
                      textAlign: TextAlign.start,
                      style: TextStyle(
                        fontSize: 20.0,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
              SizedBox(
                height: 20.0,
              ),
              Container(
                margin: EdgeInsets.only(left: 30.0, right: 30.0),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(25.0),
                  border: Border.all(
                    color: Colors.grey,
                    width: 1.0,
                  ),
                ),
                child: Padding(
                  padding: EdgeInsets.only(left: 15.0, right: 15.0),
                  child: DropdownButton(
                      padding: EdgeInsets.only(left: 25.0),
                      underline: Container(),
                      alignment: Alignment.center,
                      elevation: 1,
                      borderRadius: BorderRadius.circular(25.0),
                      dropdownColor: Colors.grey[100],
                      isExpanded: true,
                      hint: Text('대부위 선택'),
                      iconEnabledColor: Colors.grey[400],
                      value: selectedLarges,
                      items: largeOrders_1
                          .map((e) => DropdownMenuItem(
                                child: Center(child: Text(e)),
                                value: e,
                              ))
                          .toList(),
                      onChanged: isselectedorder
                          ? (value) {
                              setState(() {
                                selectedLarges = value as String;
                                setLarge(selectedLarges!);
                                isselectedlarge = true;
                                isFinal = true;
                              });
                            }
                          : null),
                ),
              ),
              SizedBox(
                height: 20.0,
              ),
              Container(
                margin: EdgeInsets.only(left: 30.0, right: 30.0),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(25.0),
                  border: Border.all(
                    color: Colors.grey,
                    width: 1.0,
                  ),
                ),
                child: Padding(
                  padding: EdgeInsets.only(left: 15.0, right: 15.0),
                  child: DropdownButton(
                      padding: EdgeInsets.only(left: 25.0),
                      underline: Container(),
                      alignment: Alignment.center,
                      elevation: 1,
                      borderRadius: BorderRadius.circular(25.0),
                      dropdownColor: Colors.grey[100],
                      isExpanded: true,
                      hint: Text('소부위 선택'),
                      iconEnabledColor: Colors.grey[400],
                      value: selectedLittles,
                      items: tableData[selectedlarge]
                          .map((e) => DropdownMenuItem(
                                child: Center(child: Text(e)),
                                value: e,
                              ))
                          .toList(),
                      onChanged: isselectedlarge
                          ? (value) {
                              setState(() {
                                selectedLittles = value as String;
                                isFinal = true;
                                setLittle(selectedLittles!);
                              });
                            }
                          : null),
                ),
              ),
              SizedBox(
                height: 30.0,
              ),
              Padding(
                padding: const EdgeInsets.only(left: 35.0),
                child: Row(
                  children: [
                    Text(
                      '관리번호',
                      textAlign: TextAlign.start,
                      style: TextStyle(
                        fontSize: 20.0,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
              SizedBox(
                height: 15.0,
              ),
              Row(
                children: [
                  Container(
                    width: 160.0,
                    height: 50.0,
                    alignment: Alignment.center,
                    margin: EdgeInsets.only(left: 30.0, right: 10.0),
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(30.0),
                      border: Border.all(
                        color: Colors.black12,
                        width: 3,
                      ),
                    ),
                    child: Text(
                      '202209191150',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 20.0,
                        fontWeight: FontWeight.w400,
                        color: Colors.black38,
                      ),
                    ),
                  ),
                  Container(
                    width: 20.0,
                    child: Divider(
                      color: Colors.grey[400],
                      thickness: 1.0,
                    ),
                  ),
                  Container(
                    width: 40.0,
                    height: 50.0,
                    alignment: Alignment.center,
                    margin: EdgeInsets.only(left: 10.0, right: 10.0),
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(30.0),
                      border: Border.all(
                        color: Colors.black12,
                        width: 3,
                      ),
                    ),
                    child: Text(
                      '$selectedlarge$selectedlittle',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 20.0,
                        fontWeight: FontWeight.w400,
                        color: Colors.black38,
                      ),
                    ),
                  ),
                ],
              ),
              SizedBox(
                height: 15.0,
              ),
              Padding(
                padding: const EdgeInsets.all(20.0),
                child: SizedBox(
                  height: 55,
                  width: 350,
                  child: ElevatedButton(
                    onPressed: isFinal ? () => {} : null,
                    child: Text('다음'),
                    style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.grey[800],
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10.0),
                        )),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
