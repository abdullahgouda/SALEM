import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/cubits/auth/auth_cubit.dart';
import 'package:salem/view/modules/common/profile_option_tile.dart';

class Profile extends StatelessWidget {
  const Profile({super.key});

  @override
  Widget build(BuildContext context) {
    final authState = context.watch<AuthCubit>().state;

    String userName = "Logging Out...";

    if (authState is AuthAuthenticated) {
      userName = authState.user.username; // أو fullName أو username
    }
    return SafeArea(
      child: Padding(
        padding: EdgeInsets.symmetric(horizontal: 30.w),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: EdgeInsets.only(top: 35.h),
              child: Center(
                child: ShaderMask(
                  shaderCallback: (mainGradient_green).createShader,
                  blendMode: BlendMode.srcIn,
                  child: Text(
                    "My Profile",
                    style: TextStyle(
                      fontSize: 24.sp,
                      fontWeight: FontWeight.w600,
                      fontFamily: 'league',
                    ),
                  ),
                ),
              ),
            ),

            SizedBox(height: 13.h),

            Center(
              child: Stack(
                clipBehavior: Clip.none,
                children: [
                  CircleAvatar(
                    radius: 52.r,
                    backgroundColor: Colors.grey.shade300,
                    backgroundImage: Image.asset(
                      'assets/vectors/avatar.png',
                      fit: BoxFit.cover,
                    ).image,
                  ),
                  Positioned(
                    right: -3.w,
                    bottom: 4.h,
                    child: Container(
                      width: 28.w,
                      height: 28.h,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        gradient: mainGradient_green,
                      ),
                      child: SvgPicture.asset(
                        'assets/vectors/pen_icon.svg',
                        width: 12.6.w,
                        height: 18.2.h,
                        fit: BoxFit.none,
                      ),
                    ),
                  ),
                ],
              ),
            ),

            SizedBox(height: 16.43.h),

            Center(
              child: Text(
                userName,
                style: TextStyle(
                  fontSize: 24.sp,
                  fontWeight: FontWeight.w600,
                  color: Colors.black,
                  fontFamily: 'league',
                ),
              ),
            ),

            SizedBox(height: 40.h),

            const ProfileOptionTile(icon: 'profile2_icon', title: "Profile"),
            const ProfileOptionTile(icon: 'lock_icon', title: "Privacy Policy"),
            const ProfileOptionTile(icon: 'settings_icon', title: "Settings"),
            const ProfileOptionTile(icon: 'help_icon', title: "Help"),
            ProfileOptionTile(
              icon: 'exit_icon',
              title: "Logout",
              showArrow: false,
              onTap: () {
                context.read<AuthCubit>().logout();
              },
            ),
          ],
        ),
      ),
    );
  }
}
