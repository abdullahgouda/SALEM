import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/cubits/auth/auth_cubit.dart';
import 'package:salem/view/modules/common/back_arrow.dart';
import 'package:salem/view/modules/common/main_button.dart';

class OtpVerify extends StatefulWidget {
  const OtpVerify({super.key});

  @override
  State<OtpVerify> createState() => _OtpVerifyState();
}

class _OtpVerifyState extends State<OtpVerify> {
  final List<TextEditingController> _controllers = List.generate(
    6,
    (index) => TextEditingController(),
  );

  final List<FocusNode> _focusNodes = List.generate(6, (index) => FocusNode());

  Timer? _timer;
  int _remainingSeconds = 60;
  bool _canResend = false;
  String email = '';
  @override
  void initState() {
    super.initState();
    _startTimer();
  }

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

  void _startTimer() async {
    _remainingSeconds = 60;
    _canResend = false;
    _timer?.cancel();

    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      if (_remainingSeconds > 0) {
        setState(() {
          _remainingSeconds--;
        });
      } else {
        setState(() {
          _canResend = true;
        });
        timer.cancel();
      }
    });
  }

  String _formatTime() {
    int minutes = _remainingSeconds ~/ 60;
    int seconds = _remainingSeconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:${seconds.toString().padLeft(2, '0')}';
  }

  @override
  void dispose() {
    _timer?.cancel();
    for (var controller in _controllers) {
      controller.dispose();
    }
    for (var node in _focusNodes) {
      node.dispose();
    }
    super.dispose();
  }

  String getOtp() {
    return _controllers.map((c) => c.text).join();
  }

  @override
  Widget build(BuildContext context) {
    return BlocConsumer<AuthCubit, AuthState>(
      listenWhen: (previous, current) {
        return current is AuthError || current is AuthOtpSucess;
      },
      listener: (context, state) {
        if (state is AuthError) {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text(state.message)));
        }
        if (state is AuthOtpSucess) {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text(state.message)));
          Navigator.pushReplacementNamed(
            context,
            '/resetPassword',
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
              "Verification",
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
                  'Enter the verification code',
                  style: TextStyle(
                    color: Color(0xff1B4374),
                    fontFamily: 'league',
                    fontSize: 24.sp,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                SizedBox(height: 8.h),
                Text(
                  'We have sent the confirmation code to the following',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Color(0xff1B4374),
                    fontSize: 14.sp,
                    fontFamily: 'league',
                  ),
                ),
                Text(
                  email,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Color(0xff1B4374),
                    fontSize: 14.sp,
                    fontFamily: 'league',
                    fontWeight: FontWeight.w700,
                  ),
                ),
                SizedBox(height: 38.h),

                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: List.generate(6, (index) => _buildOtpField(index)),
                ),
                SizedBox(height: 24.h),
                state is AuthLoading
                    ? Padding(
                        padding: EdgeInsets.only(top: 50.h),
                        child: CircularProgressIndicator(),
                      )
                    : Column(
                        children: [
                          Text(
                            _formatTime(),
                            style: TextStyle(
                              color: Color(0xffA34231),
                              fontFamily: 'league',
                              fontSize: 14.sp,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          SizedBox(height: 8.h),

                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text(
                                'Didn\'t receive a code?',
                                style: TextStyle(
                                  color: Color(0xffA34231),
                                  fontFamily: 'league',
                                  fontSize: 14.sp,
                                ),
                              ),
                              SizedBox(width: 8.w),
                              GestureDetector(
                                onTap: () {
                                  if (_canResend) {
                                    context.read<AuthCubit>().getOtp(email);
                                    _startTimer();
                                    if (state is AuthWaitingOtp) {
                                      ScaffoldMessenger.of(
                                        context,
                                      ).showSnackBar(
                                        SnackBar(content: Text(state.message)),
                                      );
                                    }
                                  }
                                },
                                child: Text(
                                  'Request a new code',
                                  style: TextStyle(
                                    color: _canResend
                                        ? Color(0xffA34231)
                                        : Color(
                                            0xffA34231,
                                          ).withValues(alpha: 0.5),
                                    fontFamily: 'league',
                                    fontSize: 14.sp,
                                    fontWeight: FontWeight.w700,
                                  ),
                                ),
                              ),
                            ],
                          ),

                          SizedBox(height: 24.h),
                          MainButton(
                            text: 'Send verification code',
                            font_family: 'din',
                            gradient: mainGradient_green,
                            borderRadius: 1000.r,
                            width: 342.w,
                            height: 52.h,
                            bottom_padding: 8.h,
                            fontSize: 24.sp,
                            ontap: () {
                              String otp = getOtp();
                              context.read<AuthCubit>().verifyOtp(email, otp);
                            },
                          ),
                        ],
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
                      ontap: () => Navigator.pushNamed(context, '/welcome'),
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

  Widget _buildOtpField(int index) {
    return Container(
      width: 50.w,
      height: 50.h,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(25.r),
        border: Border.all(color: Color(0xFFECECEC), width: 1.5),
        color: Colors.white,
      ),
      child: Center(
        child: TextField(
          controller: _controllers[index],
          focusNode: _focusNodes[index],
          textAlign: TextAlign.center,
          keyboardType: TextInputType.number,
          maxLength: 1,
          style: TextStyle(
            fontSize: 20.sp,
            fontWeight: FontWeight.bold,
            color: Color(0xff1B4374),
            fontFamily: 'league',
          ),
          decoration: InputDecoration(
            counterText: '',
            border: InputBorder.none,
            contentPadding: EdgeInsets.zero,
          ),
          inputFormatters: [FilteringTextInputFormatter.digitsOnly],
          onChanged: (value) {
            if (value.isNotEmpty) {
              // انتقل للحقل التالي
              if (index < 5) {
                _focusNodes[index + 1].requestFocus();
              } else {
                // آخر حقل - اخفي الكيبورد
                _focusNodes[index].unfocus();
              }
            }
          },
          onTap: () {
            // لو ضغط على حقل والحقول اللي قبله فاضية، ارجع للأول الفاضي
            if (_controllers[index].text.isEmpty && index > 0) {
              for (int i = 0; i < index; i++) {
                if (_controllers[i].text.isEmpty) {
                  _focusNodes[i].requestFocus();
                  return;
                }
              }
            }
          },
        ),
      ),
    );
  }
}
