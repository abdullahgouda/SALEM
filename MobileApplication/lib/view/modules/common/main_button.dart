import 'package:flutter/material.dart';

class MainButton extends StatelessWidget {
  const MainButton({
    super.key,
    required this.text,
    this.width,
    this.height,
    this.borderRadius,
    this.gradient,
    this.color,
    this.top_padding,
    this.bottom_padding,
    this.left_padding,
    this.right_padding,
    this.fontSize,
    required this.ontap,
    required this.font_family,
  });
  final String font_family;
  final String text;
  final double? width;
  final double? height;
  final double? borderRadius;
  final LinearGradient? gradient;
  final Color? color;
  final double? top_padding;
  final double? bottom_padding;
  final double? left_padding;
  final double? right_padding;
  final double? fontSize;
  final VoidCallback? ontap;
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: ontap,
      child: Container(
        alignment: Alignment.center,
        width: width,
        height: height,
        decoration: BoxDecoration(
          gradient: gradient,
          color: color,
          borderRadius: BorderRadius.circular(borderRadius ?? 0),
        ),
        child: Padding(
          padding: EdgeInsets.only(
            top: top_padding ?? 0,
            bottom: bottom_padding ?? 0,
            left: left_padding ?? 0,
            right: right_padding ?? 0,
          ),
          child: Text(
            text,
            textAlign: TextAlign.center,
            textHeightBehavior: TextHeightBehavior(
              applyHeightToFirstAscent: false,
              applyHeightToLastDescent: false,
            ),
            style: TextStyle(
              color: Colors.white,
              fontSize: fontSize,
              fontFamily: font_family,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ),
    );
  }
}
// padding: const EdgeInsets.only(
//             top: 5.0,
//             bottom: 10.0,
//             left: 30.0,
//             right: 30.0,