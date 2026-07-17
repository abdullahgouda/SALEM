import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/models/tasks_model.dart';

class CompletedTaskTile extends StatelessWidget {
  const CompletedTaskTile({super.key, required this.task});
  final TaskModel task;
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 2.w),
      child: Container(
        height: 89.h,
        decoration: BoxDecoration(
          gradient: mainGradient_green,
          borderRadius: BorderRadius.circular(17.r),
        ),
        child: Padding(
          padding: EdgeInsets.symmetric(horizontal: 12.w, vertical: 5.h),
          child: Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(13.r),
              color: Colors.white,
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
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
                          padding: EdgeInsets.only(left: 17.w),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.spaceAround,
                            children: [
                              Row(
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
                                    task.type!,
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
                                    task.id.toString(),
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
                                children: [
                                  Text(
                                    'Created: ',
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
                                    task.formattedDate,
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
                                children: [
                                  Text(
                                    'Summary: ',
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
                                    task.whatWasDone!,
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
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
