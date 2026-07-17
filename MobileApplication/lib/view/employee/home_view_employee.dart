import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/cubits/auth/auth_cubit.dart';
import 'package:salem/cubits/tasks/task_cubit.dart';
import 'package:salem/view/modules/citizen_widgets/date_task_container.dart';
import 'package:salem/view/modules/employee_widgets/incoming_tasks_tile.dart';
import 'package:salem/view/modules/employee_widgets/info_employee_tile.dart';
import 'package:salem/view/modules/common/main_button.dart';
import 'package:salem/view/modules/citizen_widgets/recent_tasks_tile.dart';

class EmployeeHome extends StatelessWidget {
  const EmployeeHome({super.key});

  @override
  Widget build(BuildContext context) {
    final authState = context.watch<AuthCubit>().state;

    String userName = "John Doe";

    if (authState is AuthAuthenticated) {
      userName = authState.user.username; // أو fullName أو username
    }

    return SafeArea(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: EdgeInsets.symmetric(horizontal: 30.w),
            child: Row(
              children: [
                CircleAvatar(
                  radius: 22.r,
                  backgroundImage: Image.asset(
                    width: 40.w,
                    height: 40.h,
                    "assets/vectors/avatar.png",
                  ).image,
                ),

                SizedBox(width: 10.w),

                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "Hi, WelcomeBack",
                      style: TextStyle(
                        fontSize: 12.sp,
                        color: Color(0xff00BE9B),
                        fontFamily: 'league',
                      ),
                    ),
                    Text(
                      userName,
                      style: TextStyle(
                        fontWeight: FontWeight.w400,
                        fontSize: 14.sp,
                        fontFamily: 'league',
                      ),
                    ),
                  ],
                ),

                const Spacer(),

                Container(
                  width: 30.w,
                  height: 30.h,
                  decoration: BoxDecoration(
                    color: Color(0xffCAD6FF),
                    borderRadius: BorderRadius.circular(50.r),
                  ),
                  child: Center(
                    child: IconButton(
                      icon: Image.asset(
                        "assets/vectors/ring_icon.png",
                        width: 14.w,
                        height: 17.h,
                        fit: BoxFit.contain,
                      ),
                      onPressed: () {},
                    ),
                  ),
                ),
                SizedBox(width: 4.w),
                Container(
                  width: 30.w,
                  height: 30.h,
                  decoration: BoxDecoration(
                    color: Color(0xffCAD6FF),
                    borderRadius: BorderRadius.circular(50.r),
                  ),
                  child: Center(
                    child: IconButton(
                      icon: Image.asset(
                        "assets/vectors/settings_icon.png",
                        width: 17.w,
                        height: 17.h,
                        fit: BoxFit.contain,
                      ),
                      onPressed: () {},
                    ),
                  ),
                ),
              ],
            ),
          ),
          SizedBox(height: 26.7.h),
          BlocBuilder<TaskCubit, TaskState>(
            builder: (context, state) {
              final cubit = context.read<TaskCubit>();

              return Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  InfoTile(
                    width: 121.w,
                    height: 117.h,
                    img: "assets/vectors/Group_employee.svg",
                    title: "Total Reports Today",
                    number: cubit.totalTasksToday.toString(),
                  ),
                  SizedBox(width: 24.w),
                  InfoTile(
                    width: 83.w,
                    height: 104.h,
                    img: "assets/vectors/tick-square.svg",
                    title: "completed",
                    number: cubit.completedTasks.toString(),
                  ),
                  SizedBox(width: 24.w),
                  InfoTile(
                    width: 83.w,
                    height: 104.h,
                    img: "assets/vectors/timer-start.svg",
                    title: "pending",
                    number: cubit.pendingTasks.toString(),
                  ),
                ],
              );
            },
          ),
          SizedBox(height: 14.h),
          Padding(
            padding: EdgeInsets.only(left: 14.w),
            child: Text(
              'Incoming Reports List:',
              style: TextStyle(
                fontSize: 20.sp,
                fontWeight: FontWeight.bold,
                fontFamily: 'leauge',
              ),
            ),
          ),
          SizedBox(height: 14.h),
          Padding(
            padding: EdgeInsets.only(left: 8.w),
            child: BlocBuilder<TaskCubit, TaskState>(
              builder: (context, state) {
                if (state is TaskLoading) {
                  return Center(child: CircularProgressIndicator());
                } else if (state is TaskLoaded) {
                  final tasks = state.EmployeeTasks;
                  if (tasks.isEmpty) {
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
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: tasks.length,
                    itemBuilder: (context, index) {
                      final task = tasks[index];

                      return IncomingTasksTile(task: task);
                    },
                  );
                } else if (state is TaskError) {
                  return Center(child: Text(state.message));
                } else {
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
              },
            ),
          ),
        ],
      ),
    );
  }
}
