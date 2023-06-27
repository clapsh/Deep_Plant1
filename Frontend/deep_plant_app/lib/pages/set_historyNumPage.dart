import 'package:flutter/material.dart';
import 'package:deep_plant_app/source/historyNum_Source.dart';
import 'package:deep_plant_app/source/widgets.dart';

class HistoryNumPage extends StatefulWidget {
  const HistoryNumPage({super.key});

  @override
  State<HistoryNumPage> createState() => _HistoryNumPageState();
}

class _HistoryNumPageState extends State<HistoryNumPage> {
  historyNum_Source source = historyNum_Source();
  List<String>? largeData;
  List<List<String>>? tableData;

  String? selectedOrder; // -> 소, 돼지의 실질적 텍스트
  int orderNum = 0; // -> 소, 돼지의 편의적 정수
  bool isselectedorder = false; // -> 완료 되었는지를 확인

  String? selectedLarge; // -> 선택된 종류에 대한 대분류 텍스트
  int largeNum = 0; // -> 선택된 분류에 대한 편의적 수
  bool isselectedlarge = false; // -> 완료 되었는지를 확인

  String? selectedLittle; // -> 선택된 종류에 대한 소분류 텍스트
  int littleNum = 0; // -> 선택된 분류에 대한 편의적 수

  String? finalNumber; // -> 모든 선택 이후에 만들게 될 텍스트
  bool isFinal = false; // -> 모든 선택이 완료되었는지에 대한 분류

  void setOrder(String order, Source) {
    if (order == '소') {
      orderNum = 0;
      isselectedorder = true;
      selectedLarge = null;
      isselectedlarge = false;
      selectedLittle = null;
      finalNumber = null;
      isFinal = false;
      largeNum = 0;
      littleNum = 0;
      largeData = source.largeOrders_1;
    } else if (order == '돼지') {
      orderNum = 1;
      isselectedorder = true;
      selectedLarge = null;
      isselectedlarge = false;
      selectedLittle = null;
      finalNumber = null;
      isFinal = false;
      largeNum = 0;
      littleNum = 0;
      largeData = source.largeOrders_2;
    }
  }

  void setLarge(String large, historyNum_Source source) {
    for (int i = 0; i < largeData!.length; i++) {
      if (large == largeData![i]) {
        largeNum = i;
        isselectedlarge = true;
        selectedLittle = null;
        finalNumber = null;
        isFinal = false;
        tableData = (orderNum == 0 ? source.tableData_1 : source.tableData_2);
        littleNum = 0;
        break;
      }
    }
  }

  void setLittle(String little, historyNum_Source source) {
    for (int i = 0; i < tableData!.length; i++) {
      if (little == tableData![largeNum][i]) {
        littleNum = i;
        isFinal = true;
        break;
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    List<String> orders = source.orders;
    List<String> largeOrders_1 = source.largeOrders_1;
    List<String> largeOrders_2 = source.largeOrders_2;
    List<List<String>> tableData_1 = source.tableData_1;
    List<List<String>> tableData_2 = source.tableData_2;

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
        actions: [
          elevated(
            colorb: Colors.white,
            colori: Colors.black,
            icon: Icons.close,
          ),
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
                    value: selectedOrder,
                    items: orders
                        .map((e) => DropdownMenuItem(
                              value: e,
                              child: Center(child: Text(e)),
                            ))
                        .toList(),
                    onChanged: (value) {
                      setState(() {
                        selectedOrder = value!;
                        setOrder(selectedOrder!, source);
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
                      menuMaxHeight: 250.0,
                      alignment: Alignment.center,
                      elevation: 1,
                      borderRadius: BorderRadius.circular(25.0),
                      dropdownColor: Colors.grey[100],
                      isExpanded: true,
                      hint: Text('대부위 선택'),
                      iconEnabledColor: Colors.grey[400],
                      value: selectedLarge,
                      items: (orderNum == 0 ? largeOrders_1 : largeOrders_2)
                          .map((e) => DropdownMenuItem(
                                value: e,
                                child: Center(child: Text(e)),
                              ))
                          .toList(),
                      onChanged: isselectedorder
                          ? (value) {
                              setState(() {
                                selectedLarge = value as String;
                                setLarge(selectedLarge!, source);
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
                      menuMaxHeight: 250.0,
                      alignment: Alignment.center,
                      elevation: 1,
                      borderRadius: BorderRadius.circular(25.0),
                      dropdownColor: Colors.grey[100],
                      isExpanded: true,
                      hint: Text('소부위 선택'),
                      iconEnabledColor: Colors.grey[400],
                      value: selectedLittle,
                      items: (orderNum == 0 ? tableData_1[largeNum] : tableData_2[largeNum])
                          .map((e) => DropdownMenuItem(
                                value: e,
                                child: Center(child: Text(e)),
                              ))
                          .toList(),
                      onChanged: isselectedlarge
                          ? (value) {
                              setState(() {
                                selectedLittle = value as String;
                                setLittle(selectedLittle!, source);
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
                  SizedBox(
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
                      '$largeNum$littleNum',
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
        ),
      ),
    );
  }
}
