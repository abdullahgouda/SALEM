import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/models/tasks_model.dart';
import 'package:salem/view/employee/task_progress_view.dart';
import 'package:salem/view/modules/common/main_button.dart';
import 'package:salem/view/modules/employee_widgets/progress_bar.dart';

class CurrentTaskTile extends StatefulWidget {
  CurrentTaskTile({super.key, required this.task});

  final TaskModel task;

  @override
  State<CurrentTaskTile> createState() => _CurrentTaskTileState();
}

class _CurrentTaskTileState extends State<CurrentTaskTile> {
  String arrow = 'down';
  bool isExpanded = false;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 356.w,
      height: isExpanded ? 176.h : 73.h,
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
                              widget.task.type!,
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
                              widget.task.id!,
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
                              'Created at: ',
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
                              widget.task.formattedDate,
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
                              'Progress: ',
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
                              widget.task.status!,
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
              SizedBox(width: 3.w),
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  SizedBox(height: 13.h),
                  MainButton(
                    text: 'Continue Task',
                    ontap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) =>
                              TaskProgressView(taskId: widget.task.id!),
                        ),
                      );
                    },
                    font_family: 'league',
                    color: mainColor_navy,
                    width: 108.w,
                    height: 28.16.h,
                    fontSize: 12.sp,
                    borderRadius: 9999.r,
                  ),
                  SizedBox(height: 13.84.h),
                  Padding(
                    padding: EdgeInsets.only(right: 9.59.w),
                    child: GestureDetector(
                      onTap: () {
                        setState(() {
                          if (arrow == 'down') {
                            arrow = 'up';
                            isExpanded = true;
                          } else {
                            arrow = 'down';
                            isExpanded = false;
                          }
                        });
                      },
                      child: SvgPicture.asset(
                        'assets/vectors/${arrow}_arrow.svg',
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
          SizedBox(height: isExpanded ? 10.h : 0),
          isExpanded
              ? Container(
                  width: 328.w,
                  height: 80.h,
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(8.r),
                  ),
                  child: Padding(
                    padding: EdgeInsets.symmetric(
                      horizontal: 16.w,
                      vertical: 10.h,
                    ),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.start,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Your progress',
                          style: TextStyle(
                            fontSize: 8.sp,
                            fontWeight: FontWeight.bold,
                            color: Colors.grey.withValues(alpha: 0.8),
                          ),
                        ),
                        SizedBox(height: 8.h),
                        Text(
                          '${widget.task.progressPercentage}% complete',
                          style: TextStyle(
                            fontSize: 16.sp,
                            color: Color(0xFFD32F2F),
                            fontWeight: FontWeight.bold,
                            fontFamily: 'league',
                          ),
                        ),
                        SizedBox(height: 4.h),
                        CustomProgressBar(
                          progress: widget.task.progressPercentage / 100,
                          totalSteps: 4,
                        ),
                      ],
                    ),
                  ),
                )
              : Container(),
        ],
      ),
    );
  }
}
