import 'package:flutter/material.dart';
import 'package:deep_plant_app/source/api_Source.dart';

class dataTable extends StatefulWidget {
  const dataTable({super.key});

  @override
  State<dataTable> createState() => _dataTableState();
}

class _dataTableState extends State<dataTable> {
  var apikey = "58%2FAb40DJd41UCVYmCZM89EUoOWqT0vuObbReDQCI6ufjHIJbhZOUtQnftZErMQf6%2FgEflZVctg97VfdvvtmQw%3D%3D";
  final _formkey = GlobalKey<FormState>();

  bool isFinal = false;
  int historyNum = 0;

  final List<String> tableData = [];

  final List<String> baseData = [
    '이력번호',
    '농장',
    '도축장',
    '도축일자',
    '육류종류',
    '성별',
    '등급',
  ];

  @override
  void initState() {
    super.initState();
    print(baseData.length);
  }

  void _tryValidation() {
    final isValid = _formkey.currentState!.validate();
    if (isValid) {
      _formkey.currentState!.save();
      isFinal = true;
      print(isFinal);
      print(tableData);
      print(tableData[1].runtimeType);
    } else {
      isFinal = false;
      tableData.clear();
      print(isFinal);
      print(tableData);
    }
  }

  Future<void> fetchData(int historyNum) async {
    var pageNo = "1";
    var numOfRows = "10";
    var baseDate = "$historyNum";
    var baseTime = "0600";
    var nx = "55";
    var ny = "127";

    Source source = Source(
        baseUrl:
            "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?serviceKey=$apikey&numOfRows=$numOfRows&pageNo=$pageNo&base_date=$baseDate&base_time=$baseTime&nx=$nx&ny=$ny");

    final weatherData = await source.getJsonData();

    String totalcount = weatherData['response']['body']['pageNo'];
    String basedate = weatherData['response']['body']['items']['item'][5]['baseDate'];
    String basetime = weatherData['response']['body']['items']['item'][5]['baseTime'];
    String obsrvalue = weatherData['response']['body']['items']['item'][5]['obsrValue'];

    tableData.addAll([totalcount, basedate, basetime, obsrvalue, '', '', '']);
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
        child: Column(
          children: [
            SizedBox(height: 45.0),
            Text(
              '이력번호 입력',
              style: TextStyle(
                fontSize: 20.0,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 20.0),
            Row(
              children: [
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(12.0),
                    child: Form(
                      key: _formkey,
                      child: TextFormField(
                        key: ValueKey(1),
                        validator: (value) {
                          if (value!.isEmpty || value.length < 4) {
                            // 임시 지정!!
                            return "유효하지 않습니다!";
                          } else {
                            return null;
                          }
                        },
                        onSaved: (value) {
                          historyNum = int.parse(value!);
                        },
                        onChanged: (value) {
                          historyNum = int.parse(value);
                        },
                        decoration: InputDecoration(
                            enabledBorder: OutlineInputBorder(
                                borderSide: BorderSide(width: 0.5, color: Colors.grey),
                                borderRadius: BorderRadius.all(
                                  Radius.circular(25.0),
                                )),
                            focusedBorder: OutlineInputBorder(
                                borderSide: BorderSide(width: 0.5, color: Colors.grey),
                                borderRadius: BorderRadius.all(
                                  Radius.circular(25.0),
                                )),
                            hintText: '이력번호 입력',
                            contentPadding: EdgeInsets.all(12.0),
                            fillColor: Colors.grey[200],
                            filled: true),
                        keyboardType: TextInputType.number,
                      ),
                    ),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.only(right: 15.0),
                  child: SizedBox(
                    height: 45,
                    width: 85,
                    child: ElevatedButton(
                      onPressed: () async {
                        await fetchData(historyNum);
                        _tryValidation();
                        FocusScope.of(context).unfocus();
                        setState(() {});
                      },
                      child: Text('검색'),
                      style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.grey[800],
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(25.0),
                          )),
                    ),
                  ),
                ),
              ],
            ),
            SizedBox(
              height: isFinal ? 25.0 : 400.0,
              width: 350.0,
            ),
            if (isFinal == true) Expanded(child: View(tableData: tableData, baseData: baseData)),
            Padding(
              padding: const EdgeInsets.all(25.0),
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
    );
  }
}

class View extends StatelessWidget {
  const View({super.key, required this.tableData, required this.baseData});

  final List<String> tableData;
  final List<String> baseData;

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: baseData.length,
      itemBuilder: (context, index) {
        return Container(
          padding: const EdgeInsets.only(left: 15.0, right: 15.0),
          child: Row(
            children: [
              Flexible(
                flex: 1,
                fit: FlexFit.tight,
                child: Container(
                  height: 45.0,
                  padding: EdgeInsets.all(8.0),
                  decoration: BoxDecoration(
                    color: Colors.grey[300],
                    border: Border.all(
                      color: Colors.grey,
                      width: 0.5,
                    ),
                  ),
                  child: Row(
                    children: [
                      RichText(
                        text: TextSpan(children: [
                          WidgetSpan(
                            child: SizedBox(
                              width: 15,
                            ),
                          ),
                          TextSpan(
                            text: baseData[index],
                            style: TextStyle(
                              fontSize: 18.0,
                              color: Colors.black,
                            ),
                          ),
                        ]),
                      ),
                    ],
                  ),
                ),
              ),
              Flexible(
                flex: 2,
                fit: FlexFit.tight,
                child: Container(
                  height: 45.0,
                  padding: EdgeInsets.all(8.0),
                  decoration: BoxDecoration(
                    border: Border.all(
                      color: Colors.grey,
                      width: 0.25,
                    ),
                  ),
                  child: Row(
                    children: [
                      RichText(
                        text: TextSpan(children: [
                          WidgetSpan(
                            child: SizedBox(
                              width: 15,
                            ),
                          ),
                          TextSpan(
                            text: tableData[index],
                            style: TextStyle(
                              fontSize: 18.0,
                              color: Colors.black,
                            ),
                          ),
                        ]),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
