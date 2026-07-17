import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/cubits/auth/auth_cubit.dart';
import 'package:salem/cubits/auth/password_cubit.dart';
import 'package:salem/view/modules/common/back_arrow.dart';
import 'package:salem/view/modules/common/main_button.dart';
import 'package:salem/view/modules/common/text_form.dart';

class ResetPassword extends StatefulWidget {
  ResetPassword({super.key});

  @override
  State<ResetPassword> createState() => _ResetPasswordState();
}

class _ResetPasswordState extends State<ResetPassword> {
  final TextEditingController passwordController = TextEditingController();

  final TextEditingController confirmPasswordController =
      TextEditingController();
  String email = '';
  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    // ⭐ نجيب الإيميل من الـ arguments أول مرة بس
    if (email.isEmpty) {
      final args = ModalRoute.of(context)?.settings.arguments;
      if (args != null && args is String) {
        email = args;
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return BlocConsumer<AuthCubit, AuthState>(
      listenWhen: (previous, current) {
        return current is AuthError || current is AuthResetPasswordSucess;
      },
      listener: (context, state) {
        if (state is AuthError) {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text(state.message)));
        }
        if (state is AuthResetPasswordSucess) {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text(state.message)));
          Navigator.pop(context);
        }
      },
      builder: (context, state) {
        return Scaffold(
          appBar: AppBar(
            leading: BackArrow(),
            centerTitle: true,
            title: Text(
              "Set New Password",
              style: TextStyle(
                fontFamily: 'league',
                fontWeight: FontWeight.w500,
                fontSize: 24.sp,
                color: Color(0xff1B4374),
              ),
            ),
          ),
          body: Padding(
            padding: EdgeInsets.symmetric(horizontal: 20.w),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                SizedBox(height: 50.h),

                Text(
                  'Password',
                  style: TextStyle(
                    fontSize: 20.sp,
                    fontFamily: 'league',
                    color: mainColor_navy,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                SizedBox(height: 12.h),
                BlocBuilder<PasswordCubit, bool>(
                  builder: (context, state) {
                    return TextForm(
                      hintText: "*************",
                      txtcontroller: passwordController,
                      type: "password",
                      isPasswordVisible: state,
                      toggle_password: () {
                        context.read<PasswordCubit>().toggle();
                      },
                    );
                  },
                ),
                SizedBox(height: 31.h),

                Text(
                  'Confirm Password ',
                  style: TextStyle(
                    fontSize: 20.sp,
                    fontFamily: 'league',
                    color: mainColor_navy,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                SizedBox(height: 12.h),

                BlocBuilder<PasswordCubit, bool>(
                  builder: (context, state) {
                    return TextForm(
                      hintText: "*************",
                      txtcontroller: confirmPasswordController,
                      type: "password",
                      isPasswordVisible: state,
                      toggle_password: () {
                        context.read<PasswordCubit>().toggle();
                      },
                    );
                  },
                ),
                SizedBox(height: 44.h),
                Center(
                  child: state is AuthLoading
                      ? CircularProgressIndicator()
                      : MainButton(
                          text: 'Create new password',
                          font_family: 'din',
                          gradient: mainGradient_green,
                          borderRadius: 30.r,
                          width: 273.w,
                          height: 45.h,
                          bottom_padding: 8.h,
                          fontSize: 24.sp,
                          ontap: () {
                            context.read<AuthCubit>().resetPassword(
                              email,
                              passwordController.text,
                              confirmPasswordController.text,
                            );
                          },
                        ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
