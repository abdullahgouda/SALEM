import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';

class InfoTile extends StatelessWidget {
  InfoTile({
    super.key,
    required this.img,
    required this.title,
    required this.number,
    required this.width,
    required this.height,
  });
  final String img;
  final String title;
  final String number;
  final double width;
  final double height;
  @override
  Widget build(BuildContext context) {
    return Container(
      width: width,
      height: height,
      decoration: BoxDecoration(
        gradient: mainGradient_green,
        borderRadius: BorderRadius.circular(16.r),
      ),
      child: Padding(
        padding: EdgeInsets.symmetric(horizontal: 8.w),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            SvgPicture.asset(img),
            SizedBox(height: 10.h),
            Text(
              title,
              textAlign: TextAlign.center,
              textHeightBehavior: TextHeightBehavior(
                applyHeightToFirstAscent: false,
                applyHeightToLastDescent: false,
              ),
              style: TextStyle(
                fontSize: 12.sp,
                color: Colors.white,
                fontFamily: 'leauge',
                fontWeight: FontWeight.w900,
              ),
            ),
            SizedBox(height: 5.h),
            Text(
              number,
              textHeightBehavior: TextHeightBehavior(
                applyHeightToFirstAscent: false,
                applyHeightToLastDescent: false,
              ),
              style: TextStyle(
                fontSize: 22.sp,
                color: Colors.white,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
