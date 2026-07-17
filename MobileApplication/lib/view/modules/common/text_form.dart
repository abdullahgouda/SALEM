import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';

class TextForm extends StatelessWidget {
  TextForm({
    this.ontap,
    this.readOnly = false,
    this.toggle_password,
    this.isPasswordVisible,
    super.key,
    required this.hintText,
    required this.type,
    required this.txtcontroller,
  });
  final String hintText;
  final String type;
  final TextEditingController txtcontroller;
  final VoidCallback? toggle_password;
  final bool? isPasswordVisible;
  final bool readOnly;
  final VoidCallback? ontap;

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 45.h,
      decoration: BoxDecoration(
        color: Color(0XFFECF1FF),
        borderRadius: BorderRadius.circular(13.r),
      ),
      child: TextFormField(
        controller: txtcontroller,
        style: TextStyle(
          color: Color(0xFFA34231),
          fontSize: 20.sp,
          fontFamily: 'league',
        ),
        decoration: InputDecoration(
          hintText: hintText,

          hintStyle: TextStyle(
            color: Color(0xFFA34231),
            fontSize: 20.sp,
            fontFamily: 'league',
          ),

          border: InputBorder.none,
          contentPadding: type == 'password'
              ? EdgeInsets.only(left: 13.w, top: 12.h)
              : EdgeInsets.only(left: 13.w),
          suffixIcon: type == 'password'
              ? GestureDetector(
                  onTap: toggle_password,
                  child: SvgPicture.asset(
                    "assets/vectors/eye_icon.svg",
                    fit: BoxFit.scaleDown,
                  ),
                )
              : null,
        ),
        obscureText: type == "password" ? isPasswordVisible! : false,
        onTap: ontap,
      ),
    );
  }
}
