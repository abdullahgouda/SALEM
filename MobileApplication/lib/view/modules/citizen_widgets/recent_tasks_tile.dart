import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';

class RecentTasksTile extends StatelessWidget {
  const RecentTasksTile({
    super.key,
    required this.type,
    required this.status,
    required this.date,
  });
  final String type;
  final String status;
  final String date;
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 12, bottom: 8),
      child: Container(
        height: 63.h,
        width: 304.w,
        decoration: BoxDecoration(
          gradient: mainGradient_green,
          borderRadius: BorderRadius.circular(17.r),
        ),
        child: Row(
          children: [
            SizedBox(width: 11.w),
            Container(
              width: 193.w,
              height: 46.h,
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(13.r),
              ),
              child: Padding(
                padding: EdgeInsets.only(left: 13.w),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Text(
                          "Type: ",
                          textHeightBehavior: TextHeightBehavior(
                            applyHeightToFirstAscent: false,
                            applyHeightToLastDescent: false,
                          ),
                          style: TextStyle(
                            fontSize: 12.sp,
                            fontWeight: FontWeight.bold,
                            fontFamily: 'league',
                          ),
                        ),

                        Text(
                          type,
                          textHeightBehavior: TextHeightBehavior(
                            applyHeightToFirstAscent: false,
                            applyHeightToLastDescent: false,
                          ),
                          style: TextStyle(
                            fontSize: 12.sp,
                            fontFamily: 'league',
                          ),
                        ),
                      ],
                    ),
                    Row(
                      children: [
                        Text(
                          "Status: ",
                          textHeightBehavior: TextHeightBehavior(
                            applyHeightToFirstAscent: false,
                            applyHeightToLastDescent: false,
                          ),
                          style: TextStyle(
                            fontSize: 12.sp,
                            fontWeight: FontWeight.bold,
                            fontFamily: 'league',
                          ),
                        ),
                        Text(
                          status,
                          textHeightBehavior: TextHeightBehavior(
                            applyHeightToFirstAscent: false,
                            applyHeightToLastDescent: false,
                          ),
                          style: TextStyle(
                            fontSize: 12.sp,
                            fontFamily: 'league',
                          ),
                        ),
                      ],
                    ),
                    Row(
                      children: [
                        Text(
                          "Date: ",
                          textHeightBehavior: TextHeightBehavior(
                            applyHeightToFirstAscent: false,
                            applyHeightToLastDescent: false,
                          ),
                          style: TextStyle(
                            fontSize: 12.sp,
                            fontWeight: FontWeight.bold,
                            fontFamily: 'league',
                          ),
                        ),
                        Text(
                          date,
                          textHeightBehavior: TextHeightBehavior(
                            applyHeightToFirstAscent: false,
                            applyHeightToLastDescent: false,
                          ),
                          style: TextStyle(
                            fontSize: 12.sp,
                            fontFamily: 'league',
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            SizedBox(width: 3.w),
            Container(
              width: 43.w,
              height: 18.h,
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(15),
              ),
              child: SvgPicture.asset(
                "assets/vectors/location_icon.svg",
                width: 13.w,
                height: 14.h,
                fit: BoxFit.none,
              ),
            ),
            SizedBox(width: 6.w),
            Container(
              width: 43.w,
              height: 18.h,
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(15),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SvgPicture.asset(
                    "assets/vectors/comments_icon.svg",
                    width: 8.71.w,
                    height: 8.71.h,
                    fit: BoxFit.none,
                  ),
                  SizedBox(width: 5.29.w),
                  Text(
                    '15',
                    style: TextStyle(
                      fontSize: 12.sp,
                      fontFamily: 'league',
                      fontWeight: FontWeight.w300,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
