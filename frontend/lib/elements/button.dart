import 'package:flutter/material.dart';
import 'package:frontend/const.dart';
import 'package:google_fonts/google_fonts.dart';

class CustomButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final int colorType;
  final double fontSize;
  final double padding;
  final double borderRadius;
  final bool header;
  final double? width;
  final double? height;

  const CustomButton({
    Key? key,
    required this.text,
    this.onPressed,
    this.colorType = 1,
    this.fontSize = 24.0,
    this.padding = 0,
    this.borderRadius = 0,
    this.header = false,
    this.width,
    this.height,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final Color textColor;
    final Color bgColor;
    if (colorType == 1) {
      textColor = kTextColor;
      bgColor = kAccentColor1;
    } else if (colorType == 2) {
      textColor = kTextColor;
      bgColor = kAccentColor2;
    } else {
      textColor = kAccentColor2;
      bgColor = kAccentColor3;
    }
    return Padding(
      padding: EdgeInsets.all(padding),
      child: SizedBox(
        width: width,
        height: height,
        child: TextButton(
          style: TextButton.styleFrom(
            backgroundColor: bgColor,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(borderRadius),
              side: BorderSide(color: kTextColor, width: 2.0),
            ),
          ),
          onPressed:
              onPressed ??
              () {
                ScaffoldMessenger.of(
                  context,
                ).showSnackBar(SnackBar(content: Text('$text button pressed')));
              },
          child: Text(
            text,
            style:
                header
                    ? GoogleFonts.righteous(
                      fontSize: fontSize,
                      color: textColor,
                    )
                    : GoogleFonts.inter(fontSize: fontSize, color: textColor),
          ),
        ),
      ),
    );
  }
}
