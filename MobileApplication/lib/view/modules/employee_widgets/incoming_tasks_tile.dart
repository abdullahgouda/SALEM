import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/models/tasks_model.dart';
import 'package:salem/view/employee/task_details_view.dart';
import 'package:salem/view/modules/common/main_button.dart';

class IncomingTasksTile extends StatelessWidget {
  const IncomingTasksTile({super.key, required this.task});
  final TaskModel task;
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(bottom: 10.h, right: 8.w),
      child: Container(
        width: 344.w,
        height: 75.h,
        decoration: BoxDecoration(
          gradient: mainGradient_green,
          borderRadius: BorderRadius.circular(17.r),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            SizedBox(width: 9.w),
            Container(
              width: 196.w,
              height: 54.7.h,
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(13.r),
              ),
              child: Padding(
                padding: EdgeInsets.only(left: 12.19.w),
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
                            fontFamily: 'league',
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        Text(
                          task.type!,
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
                            fontFamily: 'league',
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        Text(
                          task.status!,
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
                      mainAxisAlignment: MainAxisAlignment.start,
                      children: [
                        Text(
                          "Location: ",
                          textHeightBehavior: TextHeightBehavior(
                            applyHeightToFirstAscent: false,
                            applyHeightToLastDescent: false,
                          ),
                          style: TextStyle(
                            fontSize: 12.sp,
                            fontFamily: 'league',
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        Expanded(
                          child: Text(
                            task.location!,
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                            style: TextStyle(
                              fontSize: 12.sp,
                              fontFamily: 'league',
                              height: 1.0,
                            ),
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
                            fontFamily: 'league',
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        Text(
                          task.formattedDate,
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
            SizedBox(width: 50.w),
            GestureDetector(
              child: Container(
                width: 78.w,
                height: 20.h,
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(18.r),
                ),
                child: Center(
                  child: Text(
                    "View Details",
                    style: TextStyle(
                      color: mainColor_navy,
                      fontSize: 12.sp,
                      fontFamily: 'league',
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
              onTap: () => Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => ReportDetails(task: task),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
