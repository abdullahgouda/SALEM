import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/cubits/auth/auth_cubit.dart';
import 'package:salem/view/modules/common/back_arrow.dart';
import 'package:salem/view/modules/common/main_button.dart';

class ForgetPasswordPage extends StatelessWidget {
  ForgetPasswordPage({super.key});
  final TextEditingController _controller = TextEditingController();
  @override
  Widget build(BuildContext context) {
    return BlocConsumer<AuthCubit, AuthState>(
      listenWhen: (previous, current) {
        return current is AuthError || current is AuthWaitingOtp;
      },
      listener: (context, state) {
        if (state is AuthError) {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text(state.message)));
        }
        if (state is AuthWaitingOtp) {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text(state.message)));
          Navigator.pushReplacementNamed(
            context,
            '/otpVerify',
            arguments: state.email,
          );
        }
      },
      builder: (context, state) {
        return Scaffold(
          appBar: AppBar(
            leading: BackArrow(),
            centerTitle: true,
            title: Text(
              "Forget Password",
              style: TextStyle(
                fontFamily: 'league',
                fontWeight: FontWeight.w500,
                fontSize: 24.sp,
                color: Color(0xff1B4374),
              ),
            ),
          ),
          body: Padding(
            padding: EdgeInsets.symmetric(horizontal: 9.w),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                SizedBox(height: 144.h),

                Container(
                  width: 60.w,
                  height: 60.h,
                  decoration: BoxDecoration(
                    color: Color(0xff0A4438).withValues(alpha: 0.1),
                    shape: BoxShape.circle,
                  ),
                  child: Center(
                    child: SvgPicture.asset("assets/vectors/forget_pass.svg"),
                  ),
                ),
                SizedBox(height: 8.h),
                Text(
                  'Password Reset',
                  style: TextStyle(
                    color: Color(0xff1B4374),
                    fontFamily: 'league',
                    fontSize: 24.sp,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                SizedBox(height: 8.h),

                Text(
                  'Enter your email address to recover your password!',
                  style: TextStyle(
                    color: Color(0xffA34231),
                    fontSize: 14.sp,
                    fontFamily: 'league',
                  ),
                ),
                SizedBox(height: 51.h),

                Container(
                  decoration: BoxDecoration(
                    color: Color(0XFFFFFFFF),
                    borderRadius: BorderRadius.circular(68.r),
                    border: Border.all(color: Color(0XFFECECEC)),
                  ),
                  child: Padding(
                    padding: EdgeInsets.symmetric(
                      horizontal: 24.w,
                      vertical: 12.h,
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,

                      children: [
                        Text(
                          'Email',
                          style: TextStyle(
                            color: Color(0xFF1B4374),
                            fontSize: 12.sp,
                            fontFamily: 'league',
                          ),
                          textHeightBehavior: TextHeightBehavior(
                            applyHeightToFirstAscent: false,
                            applyHeightToLastDescent: false,
                          ),
                        ),
                        TextFormField(
                          controller: _controller,
                          style: TextStyle(
                            color: Color(0xFFA34231),
                            fontSize: 12.sp,
                            fontFamily: 'league',
                          ),
                          decoration: InputDecoration(
                            hintStyle: TextStyle(
                              color: Color(0xFFA34231),
                              fontSize: 12.sp,
                              fontFamily: 'league',
                            ),
                            contentPadding: EdgeInsets.zero,
                            isDense: true,
                            border: InputBorder.none,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                SizedBox(height: 24.h),

                Center(
                  child: state is AuthLoading
                      ? CircularProgressIndicator()
                      : MainButton(
                          text: 'Send verification code',
                          font_family: 'din',
                          gradient: mainGradient_green,
                          borderRadius: 1000.r,
                          width: 342.w,
                          height: 52.h,
                          bottom_padding: 8.h,
                          fontSize: 24.sp,
                          ontap: () {
                            context.read<AuthCubit>().getOtp(_controller.text);
                          },
                        ),
                ),
                Spacer(),

                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'Remember your password?',
                      style: TextStyle(
                        color: Color(0xff1B4374),
                        fontFamily: 'league',
                        fontSize: 14.sp,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                    MainButton(
                      text: 'Log In !',
                      font_family: 'din',
                      gradient: mainGradient_green,
                      borderRadius: 100.r,
                      width: 119.w,
                      height: 51.h,
                      bottom_padding: 8.h,
                      fontSize: 20.sp,
                      ontap: () => Navigator.pop(context),
                    ),
                  ],
                ),
                SizedBox(height: 14.h),
              ],
            ),
          ),
        );
      },
    );
  }
}
