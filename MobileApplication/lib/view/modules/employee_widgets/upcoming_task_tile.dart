import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

import 'package:salem/core/constans.dart';
import 'package:salem/view/modules/common/main_button.dart';

class UpcomingTasksTile extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      width: 356.w,
      height: 73.h,
      decoration: BoxDecoration(
        gradient: mainGradient_green,
        borderRadius: BorderRadius.circular(17.r),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              SizedBox(width: 6.w),
              Padding(
                padding: EdgeInsets.only(top: 9.h),
                child: Container(
                  width: 235.w,
                  height: 56.32.h,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(13.r),
                    color: Colors.white,
                  ),
                  child: Padding(
                    padding: EdgeInsets.only(left: 14.16.w),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Type: ',
                              style: TextStyle(
                                fontFamily: 'league',
                                fontSize: 12.sp,
                                fontWeight: FontWeight.bold,
                              ),
                              textHeightBehavior: TextHeightBehavior(
                                applyHeightToFirstAscent: false,
                                applyHeightToLastDescent: false,
                              ),
                            ),
                            Text(
                              'task.type',
                              style: TextStyle(
                                fontFamily: 'league',
                                fontSize: 12.sp,
                              ),
                              textHeightBehavior: TextHeightBehavior(
                                applyHeightToFirstAscent: false,
                                applyHeightToLastDescent: false,
                              ),
                            ),
                            SizedBox(width: 12.w),
                            Text(
                              'Id: ',
                              style: TextStyle(
                                fontFamily: 'league',
                                fontSize: 12.sp,
                                fontWeight: FontWeight.bold,
                              ),
                              textHeightBehavior: TextHeightBehavior(
                                applyHeightToFirstAscent: false,
                                applyHeightToLastDescent: false,
                              ),
                            ),
                            Text(
                              'task.id.toString()',
                              style: TextStyle(
                                fontFamily: 'league',
                                fontSize: 12.sp,
                              ),
                              textHeightBehavior: TextHeightBehavior(
                                applyHeightToFirstAscent: false,
                                applyHeightToLastDescent: false,
                              ),
                            ),
                          ],
                        ),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.start,
                          children: [
                            Text(
                              'Status: ',
                              style: TextStyle(
                                fontFamily: 'league',
                                fontSize: 12.sp,
                                fontWeight: FontWeight.bold,
                              ),
                              textHeightBehavior: TextHeightBehavior(
                                applyHeightToFirstAscent: false,
                                applyHeightToLastDescent: false,
                              ),
                            ),
                            Text(
                              'task.status',
                              style: TextStyle(
                                fontFamily: 'league',
                                fontSize: 12.sp,
                              ),
                              textHeightBehavior: TextHeightBehavior(
                                applyHeightToFirstAscent: false,
                                applyHeightToLastDescent: false,
                              ),
                            ),
                          ],
                        ),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.start,
                          children: [
                            Text(
                              'Next Step ETA: ',
                              style: TextStyle(
                                fontFamily: 'league',
                                fontSize: 12.sp,
                                fontWeight: FontWeight.bold,
                              ),
                              textHeightBehavior: TextHeightBehavior(
                                applyHeightToFirstAscent: false,
                                applyHeightToLastDescent: false,
                              ),
                            ),
                            Text(
                              'task.nextStepETA',
                              style: TextStyle(
                                fontFamily: 'league',
                                fontSize: 12.sp,
                              ),
                              textHeightBehavior: TextHeightBehavior(
                                applyHeightToFirstAscent: false,
                                applyHeightToLastDescent: false,
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              SizedBox(width: 16.w),

              Padding(
                padding: EdgeInsets.only(top: 14.h),
                child: MainButton(
                  text: 'Reminder',
                  ontap: () {},
                  font_family: 'league',
                  color: mainColor_navy,
                  width: 83.w,
                  height: 23.h,
                  fontSize: 12.sp,
                  borderRadius: 9999.r,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
