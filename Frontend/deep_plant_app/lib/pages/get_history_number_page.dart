import 'package:flutter/material.dart';
import 'package:deep_plant_app/source/api_Source.dart';

class GetHistoryNumber extends StatefulWidget {
  const GetHistoryNumber({super.key});

  @override
  State<GetHistoryNumber> createState() => _GetHistoryNumberState();
}

class _GetHistoryNumberState extends State<GetHistoryNumber> {
  var apikey =
      "58%2FAb40DJd41UCVYmCZM89EUoOWqT0vuObbReDQCI6ufjHIJbhZOUtQnftZErMQf6%2FgEflZVctg97VfdvvtmQw%3D%3D";
  final _formkey = GlobalKey<FormState>();
  final TextEditingController _textEditingController = TextEditingController();

  bool isFinal = false;
  bool isValue = false;
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
  }

  void _tryValidation() {
    final isValid = _formkey.currentState!.validate();
    if (isValid) {
      _formkey.currentState!.save();
      isValue = true;
    } else {
      isValue = false;
      isFinal = false;
      tableData.clear();
    }
  }

  Future<void> fetchData(int historyNum) async {
    var pageNo = "1";
    var numOfRows = "10";
    var baseDate = "$historyNum";
    var baseTime = "0600";
    var nx = "55";
    var ny = "127";
    tableData.clear();

    try {
      Source source = Source(
          baseUrl:
              "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?serviceKey=$apikey&numOfRows=$numOfRows&pageNo=$pageNo&base_date=$baseDate&base_time=$baseTime&nx=$nx&ny=$ny");

      final weatherData = await source.getJsonData();

      String totalcount = weatherData['response']['body']['pageNo'];
      String basedate =
          weatherData['response']['body']['items']['item'][5]['baseDate'];
      String basetime =
          weatherData['response']['body']['items']['item'][5]['baseTime'];
      String obsrvalue =
          weatherData['response']['body']['items']['item'][5]['obsrValue'];
      String category =
          weatherData['response']['body']['items']['item'][5]['category'];
      String nxx = weatherData['response']['body']['items']['item'][5]['nx'];
      String nyy = weatherData['response']['body']['items']['item'][5]['ny'];

      tableData.addAll(
          [totalcount, basedate, basetime, obsrvalue, category, nxx, nyy]);
      isFinal = true;
    } catch (e) {
      tableData.clear();
      isFinal = false;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('이력번호가 잘못되었습니다!'),
          backgroundColor: Colors.yellow,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0.0,
        foregroundColor: Colors.black,
        actions: [
          ElevatedButton(
            onPressed: () {},
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.white,
              elevation: 0.0,
            ),
            child: Icon(
              Icons.close,
              color: Colors.black,
              size: 35.0,
            ),
          ),
        ],
      ),
      body: GestureDetector(
        onTap: () => FocusScope.of(context).unfocus(),
        child: Column(
          children: [
            Text(
              '이력번호 입력',
              style: TextStyle(
                fontSize: 20.0,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 15.0),
            Row(
              children: [
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(12.0),
                    child: Form(
                      key: _formkey,
                      child: TextFormField(
                        controller: _textEditingController,
                        maxLength: 12,
                        validator: (value) {
                          if (value!.isEmpty || value.length < 8) {
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
                                borderSide:
                                    BorderSide(width: 0.5, color: Colors.grey),
                                borderRadius: BorderRadius.all(
                                  Radius.circular(25.0),
                                )),
                            focusedBorder: OutlineInputBorder(
                                borderSide:
                                    BorderSide(width: 0.5, color: Colors.grey),
                                borderRadius: BorderRadius.all(
                                  Radius.circular(25.0),
                                )),
                            errorBorder: OutlineInputBorder(
                                borderSide:
                                    BorderSide(width: 0.5, color: Colors.grey),
                                borderRadius: BorderRadius.all(
                                  Radius.circular(25.0),
                                )),
                            focusedErrorBorder: OutlineInputBorder(
                                borderSide:
                                    BorderSide(width: 0.5, color: Colors.grey),
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
                Column(children: [
                  Padding(
                    padding: EdgeInsets.only(right: 15.0),
                    child: SizedBox(
                      height: 45,
                      width: 85,
                      child: ElevatedButton(
                        onPressed: () async {
                          tableData.clear();
                          _tryValidation();
                          if (isValue) {
                            await fetchData(historyNum);
                          }
                          setState(() {
                            FocusScope.of(context).unfocus();
                            _textEditingController.clear();
                          });
                        },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.grey[800],
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(25.0),
                          ),
                        ),
                        child: Text('검색'),
                      ),
                    ),
                  ),
                  SizedBox(
                    height: 25.0,
                  )
                ]),
              ],
            ),
            SizedBox(
              height: 10.0,
              width: 350.0,
            ),
            if (isFinal == true)
              Expanded(child: View(tableData: tableData, baseData: baseData))
            else
              Spacer(
                flex: 2,
              ),
            Padding(
              padding: const EdgeInsets.all(20.0),
              child: Transform.translate(
                offset: Offset(0, 0),
                child: SizedBox(
                  height: 55,
                  width: 350,
                  child: ElevatedButton(
                    onPressed: isFinal ? () => {} : null,
                    style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.grey[800],
                        disabledBackgroundColor: Colors.grey[400],
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(10.0),
                        )),
                    child: Text('다음'),
                  ),
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
