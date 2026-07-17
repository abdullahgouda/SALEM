import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/cubits/auth/auth_cubit.dart';
import 'package:salem/cubits/tasks/task_cubit.dart';
import 'package:salem/view/modules/citizen_widgets/date_task_container.dart';
import 'package:salem/view/modules/common/main_button.dart';
import 'package:salem/view/modules/citizen_widgets/recent_tasks_tile.dart';

class CitizenHome extends StatelessWidget {
  const CitizenHome({super.key});
  List<DateTime> getLast6Days() {
    final now = DateTime.now();

    return List.generate(6, (index) {
      return now.subtract(Duration(days: 5 - index));
    });
  }

  bool isSameDay(DateTime a, DateTime b) {
    return a.year == b.year && a.month == b.month && a.day == b.day;
  }

  String _getDayName(DateTime date) {
    const days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
    return days[date.weekday % 7];
  }

  @override
  Widget build(BuildContext context) {
    final authState = context.watch<AuthCubit>().state;

    String userName = "John Doe";

    if (authState is AuthAuthenticated) {
      userName = authState.user.username;
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
                        fit: BoxFit.cover,
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
                        fit: BoxFit.cover,
                      ),
                      onPressed: () {},
                    ),
                  ),
                ),
              ],
            ),
          ),
          SizedBox(height: 21.73.h),
          Container(
            height: 185.h,
            width: double.infinity,
            decoration: const BoxDecoration(color: Color(0xD4A34231)),
            child: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      BlocBuilder<TaskCubit, TaskState>(
                        builder: (context, state) {
                          List tasks = [];
                          final days = getLast6Days();
                          if (state is TaskLoaded) {
                            tasks = state.CitizenTasks;
                          }

                          return Row(
                            mainAxisSize: MainAxisSize.min,
                            children: List.generate(days.length, (index) {
                              final day = days[index];

                              final hasTask = tasks.any((task) {
                                final taskDate = DateTime.parse(
                                  task.date.toString(),
                                );
                                return isSameDay(taskDate, day);
                              });

                              return Padding(
                                padding: EdgeInsets.symmetric(horizontal: 5.w),
                                child: DateTaskContainer(
                                  date: day.day.toString(),
                                  day: _getDayName(day),
                                  active: hasTask,
                                ),
                              );
                            }),
                          );
                        },
                      ),
                    ],
                  ),
                  SizedBox(height: 19.h),
                  Container(
                    height: 73.h,
                    width: 299.w,
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(25.r),
                    ),
                    child: Center(
                      child: MainButton(
                        text: 'Creat New Report',
                        font_family: 'league',
                        ontap: () {
                          Navigator.pushNamedAndRemoveUntil(
                            context,
                            '/createTask',
                            (route) => false,
                          );
                        },
                        height: 45.h,
                        width: 273.w,
                        borderRadius: 30.r,
                        gradient: mainGradient_green,
                        fontSize: 24.sp,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          SizedBox(height: 19.h),
          Padding(
            padding: EdgeInsets.symmetric(horizontal: 15.w),
            child: Align(
              alignment: Alignment.centerLeft,
              child: Text(
                "Recent Reports:",
                style: TextStyle(fontSize: 20.sp, fontFamily: 'league'),
              ),
            ),
          ),
          SizedBox(height: 11.h),

          BlocBuilder<TaskCubit, TaskState>(
            builder: (context, state) {
              if (state is TaskLoading) {
                return Padding(
                  padding: EdgeInsets.only(top: 50.h),
                  child: const Center(
                    child: CircularProgressIndicator(color: Colors.black),
                  ),
                );
              }

              if (state is TaskLoaded) {
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

                return Column(
                  children: List.generate(
                    state.CitizenTasks.length < 5
                        ? state.CitizenTasks.length
                        : 5,
                    (index) {
                      final task = state.CitizenTasks[index];
                      DateTime dateTime = DateTime.parse(task.date!);

                      // تطلع التاريخ بس
                      String dateOnly =
                          "${dateTime.year}-${dateTime.month.toString().padLeft(2, '0')}-${dateTime.day.toString().padLeft(2, '0')}";
                      return RecentTasksTile(
                        type: task.type!,
                        status: task.status!,
                        date: dateOnly,
                      );
                    },
                  ),
                );
              }

              if (state is TaskError) {
                return Center(
                  child: Text(state.message, style: TextStyle(fontSize: 16.sp)),
                );
              }

              return const SizedBox();
            },
          ),
        ],
      ),
    );
  }
}
