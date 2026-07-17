import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:salem/core/constans.dart';

class DateTaskContainer extends StatelessWidget {
  const DateTaskContainer({
    super.key,
    required this.date,
    required this.day,
    required this.active,
  });
  final String date;
  final String day;
  final bool active;
  @override
  Widget build(BuildContext context) {
    return Container(
      width: 42.w,
      height: 64.h,
      decoration: BoxDecoration(
        color: active ? null : Colors.white,
        gradient: active ? mainGradient_green : null,
        borderRadius: BorderRadius.circular(18),
      ),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,

          children: [
            Text(
              date,
              textHeightBehavior: TextHeightBehavior(
                applyHeightToFirstAscent: false,
                applyHeightToLastDescent: false,
              ),
              style: TextStyle(
                fontSize: 24.sp,
                fontFamily: 'league',
                color: active ? Colors.white : Colors.black,
              ),
            ),
            Text(
              day,
              textHeightBehavior: TextHeightBehavior(
                applyHeightToFirstAscent: false,
                applyHeightToLastDescent: false,
              ),
              style: TextStyle(
                fontSize: 12.sp,
                fontFamily: 'league',
                fontWeight: FontWeight.w300,
                color: active ? Colors.white : Colors.black,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
