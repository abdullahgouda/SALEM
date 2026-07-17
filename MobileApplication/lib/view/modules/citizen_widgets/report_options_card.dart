import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';

class ReportOptionsCard extends StatelessWidget {
  const ReportOptionsCard({
    super.key,
    required this.title,
    required this.icon,
    required this.isSelected, this.onTap,
  });
  final String title;
  final String icon;
  final bool isSelected;
  final VoidCallback? onTap;
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 83.w,
        height: 104.h,
        decoration: BoxDecoration(
          color: isSelected ? mainColor_navy : null,
          gradient: isSelected ? null : mainGradient_green,
          borderRadius: BorderRadius.circular(16.r),
          border: Border.all(color: Color(0XFFF4F4F5), width: 3.w),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SvgPicture.asset(
              'assets/vectors/$icon.svg',
              width: 26.67.w,
              height: 33.33.h,
            ),
            SizedBox(height: 11.33.h),
            Text(
              title,
              style: TextStyle(
                fontSize: 12.sp,
                fontFamily: 'league',
                fontWeight: FontWeight.bold,
                color: isSelected
                    ? Colors.white
                    : Colors.black.withValues(alpha: 0.5),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
