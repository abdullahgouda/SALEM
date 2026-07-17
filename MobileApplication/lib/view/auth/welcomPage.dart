import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/cubits/auth/auth_cubit.dart';
import 'package:salem/view/modules/common/main_button.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class Welcompage extends StatelessWidget {
  const Welcompage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Opacity(
            opacity: 0.6,
            child: SvgPicture.asset(
              'assets/vectors/Vector.svg',
              width: double.infinity,
              height: double.infinity,
              fit: BoxFit.cover,
            ),
          ),
          Center(
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Container(
                  child: Image.asset(
                    'assets/vectors/Heading2.png',
                    height: 844.h,
                    fit: BoxFit.contain,
                  ),
                ),
                Expanded(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Image.asset(
                        'assets/logo.png',
                        width: 390.w,
                        fit: BoxFit.contain,
                      ),
                      SizedBox(height: 35.h),
                      Container(
                        child: Text(
                          'System for Accident Limitation & Emergency Management',
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            fontSize: 18.sp,
                            color: mainColor_navy,
                            fontFamily: 'din',
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                      SizedBox(height: 113.h),
                      BlocBuilder<AuthCubit, AuthState>(
                        builder: (context, state) {
                          if (context.read<AuthCubit>().user_type == '') {
                            return Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                MainButton(
                                  text: 'Citizen',
                                  font_family: 'din',
                                  fontSize: 18.sp,
                                  borderRadius: 30.r,
                                  color: mainColor_navy,
                                  width: 102.w,
                                  height: 40.h,
                                  bottom_padding: 4.h,
                                  ontap: () {
                                    context
                                        .read<AuthCubit>()
                                        .setUserType_citizen();
                                  },
                                ),
                                SizedBox(width: 11.w),
                                Text(
                                  'OR',
                                  style: TextStyle(
                                    fontSize: 20.sp,
                                    color: mainColor_navy,
                                    fontFamily: 'league',
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                SizedBox(width: 11.w),
                                MainButton(
                                  text: 'Employee',
                                  font_family: 'din',
                                  fontSize: 18.sp,
                                  borderRadius: 30.r,
                                  gradient: mainGradient_green,
                                  width: 127.w,
                                  height: 40.h,
                                  bottom_padding: 5.h,
                                  ontap: () {
                                    context
                                        .read<AuthCubit>()
                                        .setUserType_employee();
                                  },
                                ),
                              ],
                            );
                          } else if (context.read<AuthCubit>().user_type ==
                              'citizen') {
                            return Column(
                              children: [
                                MainButton(
                                  text: 'Log In',
                                  font_family: 'din',
                                  fontSize: 24.sp,
                                  borderRadius: 30.r,
                                  gradient: mainGradient_green,
                                  width: 207.w,
                                  height: 45.h,
                                  bottom_padding: 7.h,
                                  ontap: () {
                                    Navigator.pushNamed(context, '/login');
                                  },
                                ),
                                SizedBox(height: 7.h),
                                MainButton(
                                  text: 'Sign Up',
                                  font_family: 'din',
                                  fontSize: 24.sp,
                                  borderRadius: 30.r,
                                  color: mainColor_navy,
                                  width: 207.w,
                                  height: 45.h,
                                  bottom_padding: 7.h,
                                  ontap: () {
                                    Navigator.pushNamed(context, '/signup');
                                  },
                                ),
                              ],
                            );
                          } else {
                            return MainButton(
                              text: 'Log In',
                              font_family: 'din',
                              fontSize: 24.sp,
                              borderRadius: 30.r,
                              gradient: mainGradient_green,
                              width: 207.w,
                              height: 45.h,
                              bottom_padding: 7.h,
                              ontap: () {
                                Navigator.pushNamed(context, '/login');
                              },
                            );
                          }
                        },
                      ),
                    ],
                  ),
                ),
                Container(
                  child: Image.asset(
                    'assets/vectors/Heading.png',
                    height: 844.h,
                    fit: BoxFit.contain,
                  ),
                ),
              ],
            ),
          ),
          BlocBuilder<AuthCubit, AuthState>(
            builder: (context, state) {
              final cubit = context.watch<AuthCubit>();

              if (cubit.user_type == '') {
                return const SizedBox();
              }

              return Positioned(
                top: 40.h,
                left: 20.w,
                child: IconButton(
                  icon: SvgPicture.asset('assets/vectors/back_arrow.svg'),
                  onPressed: () {
                    context.read<AuthCubit>().resetUserType();
                  },
                ),
              );
            },
          ),
        ],
      ),
    );
  }
}
