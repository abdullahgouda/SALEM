import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/view/modules/common/main_button.dart';

class CancelTaskPage extends StatelessWidget {
  const CancelTaskPage({super.key, required this.Resettask});
  final VoidCallback Resettask;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            ShaderMask(
              shaderCallback: (mainGradient_green).createShader,
              blendMode: BlendMode.srcIn,
              child: Text(
                "Are you sure?",
                style: TextStyle(
                  fontSize: 24.sp,
                  fontWeight: FontWeight.w800,
                  fontFamily: 'league',
                ),
              ),
            ),
            Text(
              'You cannot undo this!',
              style: TextStyle(
                fontFamily: 'league',
                fontSize: 24.sp,
                fontWeight: FontWeight.w800,
                color: mainColor_navy,
              ),
            ),
            SizedBox(height: 205.h),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                MainButton(
                  width: 100.w,
                  height: 40.h,
                  text: 'Cancel',
                  fontSize: 16.sp,
                  font_family: 'league',
                  color: mainColor_navy,
                  borderRadius: 9999.r,
                  ontap: () {
                    Navigator.pop(context);
                  },
                ),
                SizedBox(width: 8.w),
                MainButton(
                  width: 127.w,
                  height: 40.h,
                  text: 'Delete report',
                  fontSize: 16.sp,
                  font_family: 'league',
                  gradient: mainGradient_green,
                  borderRadius: 9999.r,
                  ontap: Resettask,
                ),
              ],
            ),
            SizedBox(height: 120.h),
          ],
        ),
      ),
    );
  }
}
