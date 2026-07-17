import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:salem/cubits/auth/auth_cubit.dart';
import 'package:salem/cubits/auth/password_cubit.dart';
import 'package:salem/view/modules/common/back_arrow.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/view/modules/common/main_button.dart';
import 'package:salem/view/modules/common/text_form.dart';

class Signup extends StatelessWidget {
  Signup({super.key});
  final TextEditingController usernameController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  final TextEditingController emailController = TextEditingController();
  final TextEditingController nationalIdController = TextEditingController();
  final TextEditingController mobileNumberController = TextEditingController();
  final TextEditingController dateOfBirthController = TextEditingController();
  @override
  Widget build(BuildContext context) {
    AuthCubit authCubit = context.read<AuthCubit>();

    Future<void> pickBirthDate(BuildContext context) async {
      DateTime? pickedDate = await showDatePicker(
        context: context,
        initialDate: DateTime(2000, 1, 1),
        firstDate: DateTime(1900),
        lastDate: DateTime.now(),
      );

      if (pickedDate != null) {
        final formattedDate = authCubit.formatBirthDate(pickedDate);
        dateOfBirthController.text = formattedDate;
      }
    }

    return Scaffold(
      appBar: AppBar(
        leading: BackArrow(),
        centerTitle: true,
        title: Text(
          "New Account",
          style: TextStyle(
            color: mainColor_navy,
            fontFamily: 'league',
            fontWeight: FontWeight.bold,
            fontSize: 24.sp,
          ),
        ),
      ),
      body: BlocConsumer<AuthCubit, AuthState>(
        listener: (context, state) {
          if (state is AuthError) {
            ScaffoldMessenger.of(context).hideCurrentSnackBar();
            ScaffoldMessenger.of(
              context,
            ).showSnackBar(SnackBar(content: Text(state.message)));
          }
          if (state is AuthInitial) {
            usernameController.clear();
            passwordController.clear();
            emailController.clear();
            nationalIdController.clear();
            mobileNumberController.clear();
            dateOfBirthController.clear();
            ScaffoldMessenger.of(context).hideCurrentSnackBar();
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text("Account created successfully")),
            );
            Navigator.pushReplacementNamed(context, '/login');
          }
        },
        builder: (context, state) {
          return SingleChildScrollView(
            child: Center(
              child: Padding(
                padding: EdgeInsets.only(left: 30.w, right: 30.w, top: 10.h),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Text(
                      'user name',
                      style: TextStyle(
                        fontSize: 20.sp,
                        fontFamily: 'league',
                        color: mainColor_navy,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    TextForm(
                      hintText: "example",
                      txtcontroller: usernameController,
                      type: "text",
                    ),
                    SizedBox(height: 8.h),
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
                          toggle_password: () =>
                              context.read<PasswordCubit>().toggle(),
                        );
                      },
                    ),
                    SizedBox(height: 8.h),
                    Text(
                      'Email',
                      style: TextStyle(
                        fontSize: 20.sp,
                        fontFamily: 'league',
                        color: mainColor_navy,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    TextForm(
                      hintText: "example@example.com",
                      txtcontroller: emailController,
                      type: "email",
                    ),
                    SizedBox(height: 8.h),

                    Text(
                      'National ID',
                      style: TextStyle(
                        fontSize: 20.sp,
                        fontFamily: 'league',
                        color: mainColor_navy,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    TextForm(
                      hintText: "212345678901234",
                      txtcontroller: nationalIdController,
                      type: "phone",
                    ),
                    SizedBox(height: 8.h),
                    Text(
                      'Mobile Number',
                      style: TextStyle(
                        fontSize: 20.sp,
                        fontFamily: 'league',
                        color: mainColor_navy,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    TextForm(
                      hintText: "01234567890",
                      txtcontroller: mobileNumberController,
                      type: "phone",
                    ),
                    SizedBox(height: 8.h),
                    Text(
                      'Date Of Birth',
                      style: TextStyle(
                        fontSize: 20.sp,
                        fontFamily: 'league',
                        color: mainColor_navy,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    TextForm(
                      hintText: "YYYY-MM-DD",
                      txtcontroller: dateOfBirthController,
                      type: "date",
                      readOnly: true,
                      ontap: () {
                        pickBirthDate(context);
                      },
                    ),
                    SizedBox(height: 40.h),
                    Center(
                      child: Column(
                        children: [
                          Text(
                            'By continuing, you agree to',
                            style: TextStyle(
                              fontSize: 12.sp,
                              fontFamily: 'league',
                              color: mainColor_navy,
                            ),
                          ),

                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text(
                                'Terms of Service ',
                                style: TextStyle(
                                  fontSize: 12.sp,
                                  fontFamily: 'league',
                                  color: mainColor_green,
                                ),
                              ),
                              Text(
                                'and',
                                style: TextStyle(
                                  fontSize: 12.sp,
                                  fontFamily: 'league',
                                  color: mainColor_navy,
                                ),
                              ),
                              Text(
                                ' Privacy Policy.',
                                style: TextStyle(
                                  fontSize: 12.sp,
                                  fontFamily: 'league',
                                  color: mainColor_green,
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                    SizedBox(height: 8.h),
                    Center(
                      child: state is AuthLoading
                          ? const CircularProgressIndicator()
                          : MainButton(
                              text: 'Sign Up',
                              font_family: 'din',
                              fontSize: 24.sp,
                              gradient: mainGradient_green,
                              width: 207.w,
                              height: 45.h,
                              borderRadius: 30.r,
                              bottom_padding: 8.h,
                              ontap: () {
                                authCubit.signup({
                                  "Name": usernameController.text,
                                  "Phone_Number": mobileNumberController.text,
                                  "Email": emailController.text,
                                  "National_Id": nationalIdController.text,
                                  "Password": passwordController.text,
                                  "User_Type": "citizin",
                                  "Birthdate": dateOfBirthController.text,
                                  "username": usernameController.text,
                                });
                              },
                            ),
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
