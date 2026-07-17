import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/view/modules/common/main_button.dart';

class SuccessTaskPage extends StatelessWidget {
  const SuccessTaskPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SvgPicture.asset(
              'assets/vectors/big_success_icon.svg',
              width: 172.w,
              height: 172.h,
              fit: BoxFit.cover,
            ),
            SizedBox(height: 46.h),
            ShaderMask(
              shaderCallback: (mainGradient_green).createShader,
              blendMode: BlendMode.srcIn,
              child: Text(
                "Thank You",
                style: TextStyle(
                  fontSize: 60.sp,
                  fontWeight: FontWeight.bold,
                  fontFamily: 'league',
                ),
              ),
            ),
            Text(
              'for your contribution!',
              style: TextStyle(
                fontSize: 25.sp,
                fontFamily: 'league',
                fontWeight: FontWeight.w400,
              ),
            ),
            SizedBox(height: 166.h),
            MainButton(
              text: 'Continue',
              ontap: () {
                Navigator.pushNamedAndRemoveUntil(
                  context,
                  '/mainCitizen',
                  (route) => false,
                );
              },
              font_family: 'league',
              width: 240.19.w,
              height: 53.37.h,
              gradient: mainGradient_green,
              fontSize: 23.27.sp,
              borderRadius: 33.36.r,
            ),
          ],
        ),
      ),
    );
  }
}
