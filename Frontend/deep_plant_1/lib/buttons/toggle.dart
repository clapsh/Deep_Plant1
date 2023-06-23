import 'package:flutter/material.dart';

class MyToggleButtons extends StatefulWidget {
  final List<Widget> options;
  final List<bool> isSelected;
  final bool vertical;

  MyToggleButtons({
    required this.options,
    required this.isSelected,
    this.vertical = false,
  });

  @override
  State<MyToggleButtons> createState() => _MyToggleButtonsState();
}

class _MyToggleButtonsState extends State<MyToggleButtons> {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        SizedBox(
          height: 20,
        ),
        ToggleButtons(
          direction: widget.vertical ? Axis.vertical : Axis.horizontal,
          onPressed: (int index) {
            setState(() {
              for (int i = 0; i < widget.isSelected.length; i++) {
                widget.isSelected[i] = i == index;
              }
            });
          },
          borderRadius: const BorderRadius.all(Radius.circular(8)),
          selectedBorderColor: Colors.black,
          selectedColor: Colors.black,
          fillColor: Colors.white,
          color: Colors.black,
          constraints: const BoxConstraints(
            minHeight: 50.0,
            minWidth: 50.0,
          ),
          isSelected: widget.isSelected,
          children: widget.options,
        ),
        SizedBox(
          height: 20,
        ),
      ],
    );
  }
}
