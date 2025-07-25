import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:frontend/const.dart';

class CustomText extends StatelessWidget {
  final String text;
  final double fontSize;
  final Color color;
  final TextAlign textAlign;
  final bool header;
  final double padding;

  const CustomText({
    Key? key,
    required this.text,
    this.fontSize = 24.0,
    this.color = kTextColor,
    this.textAlign = TextAlign.start,
    this.header = false,
    this.padding = 0,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(padding),
      child: Text(
        text,
        textAlign: textAlign,
        style:
            header
                ? GoogleFonts.righteous(fontSize: fontSize, color: color)
                : GoogleFonts.inter(fontSize: fontSize, color: color),
      ),
    );
  }
}
