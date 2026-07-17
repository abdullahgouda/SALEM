import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class AlphaButton extends StatelessWidget {
  const AlphaButton({
    super.key,
    required this.width,
    required this.height,
    required this.text,
    required this.buttonColor,
    required this.textColor,
    required this.fontsize,
    required this.radius, required this.onTap,
  });
  final double width;
  final double height;
  final String text;
  final int buttonColor;
  final int textColor;
  final double fontsize;
  final double radius;
  final VoidCallback onTap;
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: width,
        height: height,
        decoration: BoxDecoration(
          color: Color(buttonColor).withValues(alpha: 0.3),
          borderRadius: BorderRadius.circular(radius),
        ),
        child: Center(
          child: Text(
            text,
            textAlign: TextAlign.center,
            style: TextStyle(
              color: Color(textColor),
              fontSize: fontsize,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      ),
    );
  }
}
