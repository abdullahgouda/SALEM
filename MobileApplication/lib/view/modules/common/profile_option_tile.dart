import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';

class ProfileOptionTile extends StatelessWidget {
  const ProfileOptionTile({
    super.key,
    required this.icon,
    required this.title,
    this.onTap,
    this.showArrow = true,
  });

  final String icon;
  final String title;
  final VoidCallback? onTap;
  final bool showArrow;
  
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(bottom: 18.h),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(18.r),
        child: Row(
          children: [
            Container(
              width: 40.w,
              height: 40.h,
              decoration: BoxDecoration(
                color: const Color(0xffDBDADE),
                shape: BoxShape.circle,
              ),
              child: SvgPicture.asset(
                'assets/vectors/$icon.svg',
                width: 18.w,
                height: 22.h,
                fit: BoxFit.none,
              ),
            ),
            SizedBox(width: 16.w),
            Expanded(
              child: Text(
                title,
                style: TextStyle(
                  fontSize: 22.sp,
                  fontWeight: FontWeight.w500,
                  color: Colors.black,
                ),
              ),
            ),
            if (showArrow)
              SvgPicture.asset(
                'assets/vectors/arrow_options_icon.svg',
                width: 12.w,
                height: 18.h,
                fit: BoxFit.none,
              ),
          ],
        ),
      ),
    );
  }
}
