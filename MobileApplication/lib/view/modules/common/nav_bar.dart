import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';

class MainBottomNavBar extends StatelessWidget {
  const MainBottomNavBar({
    super.key,
    required this.currentIndex,
    required this.onTap,
    required this.isEmployee,
  });

  final int currentIndex;
  final Function(int) onTap;
  final bool isEmployee;
  @override
  Widget build(BuildContext context) {
    final List<String> iconsEmployee = [
      'assets/vectors/home_icon.svg',
      'assets/vectors/my_tasks_icon.svg',
      'assets/vectors/notify_icon.svg',
      'assets/vectors/profile_icon.svg',
    ];
    final List<String> iconsCitizen = [
      'assets/vectors/home_icon.svg',
      'assets/vectors/my_tasks_icon.svg',
      'assets/vectors/profile_icon.svg',
    ];

    return Padding(
      padding: EdgeInsets.only(
        left: 30.w,
        right: 32.w,
        bottom: 19.h,
        top: 10.h,
      ),
      child: Container(
        height: 48.h,
        width: 298.w,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(24.r),
          gradient: mainGradient_green,
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: List.generate(
            isEmployee ? iconsEmployee.length : iconsCitizen.length,
            (index) => GestureDetector(
              onTap: () => onTap(index),

              child: SvgPicture.asset(
                isEmployee ? iconsEmployee[index] : iconsCitizen[index],
                colorFilter: ColorFilter.mode(
                  currentIndex == index ? mainColor_navy : Colors.white,
                  BlendMode.srcIn,
                ),
                width: 24.w,
                height: 24.h,
              ),
            ),
          ),
        ),
      ),
    );
  }
}
