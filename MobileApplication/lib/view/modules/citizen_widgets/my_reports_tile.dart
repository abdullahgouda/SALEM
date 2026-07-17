import 'package:flutter/material.dart';

import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/models/tasks_model.dart';

class MyReportsTile extends StatelessWidget {
  MyReportsTile({super.key, required this.task});
  final TaskModel task;
  late final DateTime dateTime = DateTime.parse(task.date!);
  late final String dateOnly =
      "${dateTime.year}-${dateTime.month.toString().padLeft(2, '0')}-${dateTime.day.toString().padLeft(2, '0')}";
  @override
  Widget build(BuildContext context) {
    return Container(
      width: 331.w,
      height: 69.h,
      decoration: BoxDecoration(
        gradient: mainGradient_green,
        borderRadius: BorderRadius.circular(17.r),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          SizedBox(width: 11.98.w),
          Container(
            width: 210.14.w,
            height: 50.38.h,
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
                        task.type!,
                        style: TextStyle(fontFamily: 'league', fontSize: 12.sp),
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
                        style: TextStyle(fontFamily: 'league', fontSize: 12.sp),
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
                        task.status!,
                        style: TextStyle(fontFamily: 'league', fontSize: 12.sp),
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
                        'Date: ',
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
                        dateOnly,
                        style: TextStyle(fontFamily: 'league', fontSize: 12.sp),
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
          SizedBox(width: 3.27.w),
          Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                width: 37.02.w,
                height: 19.71.h,
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(13.r),
                ),
                child: Center(
                  child: SvgPicture.asset(
                    'assets/vectors/brush_icon.svg',
                    width: 11.19.w,
                    height: 13.14.h,
                    fit: BoxFit.none,
                  ),
                ),
              ),
              SizedBox(height: 2.19.h),
              Container(
                width: 37.02.w,
                height: 19.71.h,
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(13.r),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    SvgPicture.asset(
                      'assets/vectors/comments_icon.svg',
                      width: 7.86.w,
                      height: 9.54.h,
                      fit: BoxFit.none,
                    ),
                    SizedBox(width: 3.03.w),
                    Text('15', style: TextStyle(fontSize: 10.sp)),
                  ],
                ),
              ),
            ],
          ),
          SizedBox(width: 4.6.w),
          task.beforeImage != null
              ? CircleAvatar(
                  radius: 28.5.r,
                  backgroundColor: Colors.grey.shade300,
                  backgroundImage: Image.network(
                    task.beforeImage!,
                    fit: BoxFit.cover,
                  ).image,
                )
              : CircleAvatar(
                  radius: 28.5.r,
                  backgroundColor: Colors.grey.shade300,
                  backgroundImage: Image.asset(
                    'assets/vectors/avatar.png',
                  ).image,
                ),
        ],
      ),
    );
  }
}
