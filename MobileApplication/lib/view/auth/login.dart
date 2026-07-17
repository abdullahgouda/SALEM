import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/cubits/auth/auth_cubit.dart';
import 'package:salem/cubits/auth/password_cubit.dart';
import 'package:salem/cubits/notifications/cubit/notifications_cubit.dart';
import 'package:salem/cubits/tasks/task_cubit.dart';
import 'package:salem/models/employee_model.dart';
import 'package:salem/view/modules/common/back_arrow.dart';
import 'package:salem/view/modules/common/main_button.dart';
import 'package:salem/view/modules/common/text_form.dart';

class LoginPage extends StatelessWidget {
  LoginPage({super.key});

  final TextEditingController firstController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    final cubit = context.watch<AuthCubit>();
    final isCitizen = cubit.user_type == 'citizen';

    return BlocConsumer<AuthCubit, AuthState>(
      listener: (context, state) {
        if (state is AuthAuthenticated) {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(const SnackBar(content: Text("Login Success")));

          if (cubit.user_type == 'citizen') {
            context.read<TaskCubit>().loadCitizenTasks();
            Navigator.pushNamedAndRemoveUntil(
              context,
              '/onboarding',
              (route) => false,
            );
          } else if (cubit.user_type == 'employee') {
            context.read<TaskCubit>().loadEmployeeTasks(
              department: (cubit.currentUser as EmployeeModel).Department,
              employeeId: (cubit.currentUser as EmployeeModel).id,
            );
            context.read<NotificationsCubit>().loadNotifications();
            Navigator.pushNamedAndRemoveUntil(
              context,
              '/mainEmployee',
              (route) => false,
            );
          }
        }

        if (state is AuthError) {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text(state.message)));
        }
      },
      builder: (context, state) {
        return Scaffold(
          appBar: AppBar(
            leading: BackArrow(),
            centerTitle: true,
            title: Text(
              "Log In",
              style: TextStyle(
                fontFamily: 'league',
                fontWeight: FontWeight.w500,
                fontSize: 24.sp,
              ),
            ),
          ),
          body: SingleChildScrollView(
            child: Padding(
              padding: EdgeInsets.only(top: 34.h, left: 30.w, right: 30.w),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "Welcome",
                    style: TextStyle(
                      fontSize: 24.sp,
                      fontFamily: 'league',
                      color: mainColor_navy,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  SizedBox(height: 83.h),

                  Text(
                    isCitizen ? 'Email Or Phone' : 'National ID',
                    style: TextStyle(
                      fontSize: 20.sp,
                      fontFamily: 'league',
                      color: mainColor_navy,
                      fontWeight: FontWeight.w500,
                    ),
                  ),

                  TextForm(
                    hintText: isCitizen
                        ? "xxx@xx.com | 01xxxxx"
                        : "21234567890123",
                    txtcontroller: firstController,
                    type: isCitizen ? "email" : "phone",
                  ),

                  SizedBox(height: 20.h),

                  Text(
                    'Password',
                    style: TextStyle(
                      fontSize: 20.sp,
                      fontFamily: 'league',
                      color: mainColor_navy,
                      fontWeight: FontWeight.w500,
                    ),
                  ),

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

                  SizedBox(height: 9.h),

                  isCitizen
                      ? Row(
                          mainAxisAlignment: MainAxisAlignment.end,
                          children: [
                            GestureDetector(
                              child: Text(
                                "Forgot password",
                                style: TextStyle(
                                  fontSize: 12.sp,
                                  fontFamily: 'league',
                                  color: mainColor_navy,
                                ),
                              ),
                              onTap: () => Navigator.pushNamed(
                                context,
                                '/forgetPassword',
                              ),
                            ),
                          ],
                        )
                      : Container(),

                  SizedBox(height: 37.h),

                  Center(
                    child: state is AuthLoading
                        ? const CircularProgressIndicator()
                        : MainButton(
                            text: 'Log In',
                            font_family: 'din',
                            gradient: mainGradient_green,
                            borderRadius: 30.r,
                            width: 207.w,
                            height: 45.h,
                            bottom_padding: 8.h,
                            fontSize: 24.sp,
                            ontap: () {
                              final authCubit = context.read<AuthCubit>();
                              final firstValue = firstController.text.trim();
                              final password = passwordController.text.trim();

                              if (firstValue.isEmpty || password.isEmpty) {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(
                                    content: Text("Please fill all fields"),
                                  ),
                                );
                                return;
                              }
                              if (isCitizen) {
                                authCubit.citizenLogin(firstValue, password);
                              } else {
                                authCubit.employeeLogin(firstValue, password);
                              }
                            },
                          ),
                  ),

                  isCitizen
                      ? Column(
                          children: [
                            SizedBox(height: 14.h),
                            Center(
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Text(
                                    'Don\'t have an account?',
                                    style: TextStyle(
                                      fontSize: 12.sp,
                                      fontFamily: 'league',
                                      color: mainColor_navy,
                                    ),
                                  ),
                                  GestureDetector(
                                    child: Text(
                                      ' Sign Up',
                                      style: TextStyle(
                                        fontSize: 12.sp,
                                        fontFamily: 'league',
                                        color: mainColor_green,
                                      ),
                                    ),
                                    onTap: () =>
                                        Navigator.pushNamed(context, '/signup'),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        )
                      : Container(),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}
