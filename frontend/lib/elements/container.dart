import 'package:flutter/material.dart';
import 'package:frontend/const.dart';

class CustomContainer extends StatelessWidget {
  final Widget child;
  final double padding;
  final int colorType;
  final double borderRadius;
  final double? width;
  final double? height;

  const CustomContainer({
    Key? key,
    required this.child,
    this.padding = 16.0,
    this.colorType = 1,
    this.borderRadius = 0,
    this.width,
    this.height,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    Color bgColor;
    Color borderColor;
    if (colorType == 1) {
      bgColor = kAccentColor1;
      borderColor = kTextColor;
    } else if (colorType == 2) {
      bgColor = kAccentColor2;
      borderColor = kTextColor;
    } else {
      bgColor = kAccentColor3;
      borderColor = kAccentColor2;
    }
    Widget container = Container(
      padding: EdgeInsets.all(padding),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(borderRadius),
        border: Border.all(color: borderColor, width: 2.0),
      ),
      child: child,
    );
    if (width != null || height != null) {
      container = SizedBox(width: width, height: height, child: container);
    }
    return container;
  }
}
