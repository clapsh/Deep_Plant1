import 'package:deep_plant_app/widgets/step_card.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class ShowStep extends StatefulWidget {
  const ShowStep({super.key});

  @override
  State<ShowStep> createState() => _ShowStepState();
}

class _ShowStepState extends State<ShowStep> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: Text('육류 등록'),
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        elevation: 0,
      ),
      body: Center(
        child: Column(
          children: [
            SizedBox(
              height: 50,
            ),
            GestureDetector(
              onTap: () => context.go('/option/show-step/insert-his-num'),
              child: StepCard(
                mainText: '육류 기본정보 입력',
                subText: '데이터를 입력해 주세요.',
                step: '1',
              ),
            ),
            GestureDetector(
              onTap: () => context.go('/logged-in'),
              child: StepCard(
                mainText: '육류 단면 촬영',
                subText: '데이터를 입력해 주세요.',
                step: '2',
              ),
            ),
            StepCard(mainText: '신선육 관능평가', subText: '데이터를 입력해 주세요.', step: '3'),
          ],
        ),
      ),
    );
  }
}
