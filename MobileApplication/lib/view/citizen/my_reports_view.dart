import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/cubits/tasks/task_cubit.dart';
import 'package:salem/view/modules/citizen_widgets/my_reports_tile.dart';

class MyReports extends StatelessWidget {
  const MyReports({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      floatingActionButton: GestureDetector(
        onTap: () => Navigator.pushNamedAndRemoveUntil(
          context,
          '/createTask',
          (route) => false,
        ),
        child: Container(
          width: 163.w,
          height: 34.h,
          decoration: BoxDecoration(
            gradient: mainGradient_green,
            borderRadius: BorderRadius.circular(9999.r),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.64),
                spreadRadius: 4,
                blurRadius: 16,
              ),
            ],
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              SvgPicture.asset(
                'assets/vectors/add_icon.svg',
                width: 20.w,
                height: 20.h,
                fit: BoxFit.none,
              ),
              SizedBox(width: 10.w),
              Text(
                'Add Report',
                textHeightBehavior: TextHeightBehavior(
                  applyHeightToFirstAscent: false,
                  applyHeightToLastDescent: false,
                ),
                style: TextStyle(
                  fontSize: 16.sp,
                  fontFamily: 'league',
                  color: Colors.white,
                ),
              ),
            ],
          ),
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Padding(
            padding: EdgeInsets.only(left: 10.w),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ShaderMask(
                  shaderCallback: (mainGradient_green).createShader,
                  blendMode: BlendMode.srcIn,
                  child: Center(
                    child: Text(
                      "My Reports",
                      style: TextStyle(
                        fontSize: 24.sp,
                        fontWeight: FontWeight.w600,
                        fontFamily: 'league',
                      ),
                    ),
                  ),
                ),
                SizedBox(height: 20.h),
                Padding(
                  padding: EdgeInsets.only(left: 85.w),
                  child: Container(
                    width: 259.w,
                    height: 33.h,
                    decoration: BoxDecoration(
                      gradient: mainGradient_green,
                      borderRadius: BorderRadius.circular(23.r),
                    ),
                    child: Row(
                      children: [
                        SizedBox(width: 5.w),
                        Container(
                          width: 26.w,
                          height: 26.h,
                          decoration: BoxDecoration(
                            color: Colors.white,
                            shape: BoxShape.circle,
                          ),
                          child: SvgPicture.asset(
                            'assets/vectors/filter_icon.svg',
                            width: 14.w,
                            height: 9.h,
                            fit: BoxFit.none,
                          ),
                        ),

                        SizedBox(width: 3.w),

                        // 📝 الـ TextField
                        Expanded(
                          child: Padding(
                            padding: EdgeInsets.only(bottom: 2.h),
                            child: TextField(
                              style: TextStyle(color: Colors.white),
                              decoration: InputDecoration(
                                hintText: "Search...",
                                hintStyle: TextStyle(color: Colors.white70),
                                border: InputBorder.none,
                              ),
                            ),
                          ),
                        ),

                        Padding(
                          padding: EdgeInsets.only(right: 9.w),
                          child: SvgPicture.asset(
                            'assets/vectors/search_icon.svg',
                            width: 15.w,
                            height: 18.h,
                            fit: BoxFit.none,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                SizedBox(height: 5.h),
                Text(
                  'List of Reports:',
                  style: TextStyle(
                    fontFamily: 'din',
                    fontSize: 20.sp,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                SizedBox(height: 9.h),
                BlocBuilder<TaskCubit, TaskState>(
                  builder: (context, state) {
                    if (state is TaskLoading) {
                      // Loading UI
                      return Column(
                        children: List.generate(5, (index) {
                          return Padding(
                            padding: EdgeInsets.only(bottom: 9.h),
                            child: Container(
                              height: 100.h,
                              decoration: BoxDecoration(
                                color: Colors.grey.shade300,
                                borderRadius: BorderRadius.circular(12.r),
                              ),
                            ),
                          );
                        }),
                      );
                    } else if (state is TaskLoaded) {
                      if (state.CitizenTasks.isEmpty) {
                        return Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Image.asset(
                              "assets/vectors/no_reports.png",
                              width: double.infinity,
                            ),
                            SizedBox(height: 43.h),
                            Text(
                              "No reports yet",
                              style: TextStyle(
                                fontSize: 32.sp,
                                fontWeight: FontWeight.bold,
                                fontFamily: 'league',
                              ),
                            ),
                          ],
                        );
                      }
                      return ListView.builder(
                        itemCount: state.CitizenTasks.length,
                        shrinkWrap: true,
                        physics: NeverScrollableScrollPhysics(),
                        itemBuilder: (context, index) {
                          final task = state.CitizenTasks[index];

                          return Padding(
                            padding: EdgeInsets.only(bottom: 9.h, right: 10.w),
                            child: MyReportsTile(task: task),
                          );
                        },
                      );
                    } else if (state is TaskError) {
                      return Text(state.message);
                    }

                    return SizedBox();
                  },
                ),
                SizedBox(height: 32.h),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
