import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/cubits/auth/auth_cubit.dart';
import 'package:salem/cubits/tasks/task_cubit.dart';
import 'package:salem/models/employee_model.dart';
import 'package:salem/models/tasks_model.dart';
import 'package:salem/view/modules/common/alpha_button.dart';

class ReportDetails extends StatelessWidget {
  const ReportDetails({super.key, required this.task});
  final TaskModel task;

  @override
  Widget build(BuildContext context) {
    return BlocConsumer<TaskCubit, TaskState>(
      listener: (context, state) {
        if (state is TaskError) {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text(state.message)));
        }
        if (state is TaskLoaded) {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text("Task updated successfully")));
          Navigator.pop(context);
        }
      },
      builder: (context, state) {
        final usercubit = context.read<AuthCubit>();
        final taskcubit = context.read<TaskCubit>();
        return Scaffold(
          appBar: AppBar(
            title: ShaderMask(
              shaderCallback: (mainGradient_green).createShader,
              blendMode: BlendMode.srcIn,
              child: Text(
                "Report Details",
                style: TextStyle(
                  fontSize: 16.sp,
                  fontWeight: FontWeight.w900,
                  fontFamily: 'league',
                ),
              ),
            ),
            centerTitle: true,
            leading: Center(
              child: GestureDetector(
                onTap: () => Navigator.pop(context),
                child: SizedBox(
                  width: 16.w,
                  height: 16.h,
                  child: SvgPicture.asset(
                    'assets/vectors/long_back_arrow.svg',
                    fit: BoxFit.contain,
                  ),
                ),
              ),
            ),
          ),
          body: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Padding(
                  padding: EdgeInsets.only(left: 14.w),
                  child: Container(
                    width: 331.w,
                    height: 67.h,
                    decoration: BoxDecoration(
                      gradient: mainGradient_green,
                      borderRadius: BorderRadius.circular(17.r),
                    ),
                    child: Center(
                      child: Container(
                        width: 307.w,
                        height: 50.h,
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(13.r),
                        ),
                        child: Padding(
                          padding: EdgeInsets.symmetric(
                            horizontal: 14.w,
                            vertical: 7.h,
                          ),
                          child: Row(
                            children: [
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    children: [
                                      Text(
                                        'Report: ',
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
                                        '#${task.id}',
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
                                    ],
                                  ),
                                  Row(
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
                                ],
                              ),
                              SizedBox(width: 15.w),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Row(
                                      children: [
                                        Text(
                                          'Status: ',
                                          style: TextStyle(
                                            fontFamily: 'league',
                                            fontSize: 12.sp,
                                            fontWeight: FontWeight.bold,
                                          ),
                                          textHeightBehavior:
                                              TextHeightBehavior(
                                                applyHeightToFirstAscent: false,
                                                applyHeightToLastDescent: false,
                                              ),
                                        ),
                                        Text(
                                          task.status!,
                                          style: TextStyle(
                                            fontFamily: 'league',
                                            fontSize: 12.sp,
                                          ),
                                          textHeightBehavior:
                                              TextHeightBehavior(
                                                applyHeightToFirstAscent: false,
                                                applyHeightToLastDescent: false,
                                              ),
                                        ),
                                      ],
                                    ),
                                    Row(
                                      children: [
                                        Text(
                                          'Location: ',
                                          style: TextStyle(
                                            fontFamily: 'league',
                                            fontSize: 12.sp,
                                            fontWeight: FontWeight.bold,
                                          ),
                                          textHeightBehavior:
                                              TextHeightBehavior(
                                                applyHeightToFirstAscent: false,
                                                applyHeightToLastDescent: false,
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
                                              height: 1,
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
                                    Row(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      mainAxisAlignment:
                                          MainAxisAlignment.start,
                                      children: [
                                        Text(
                                          'Priority: ',
                                          style: TextStyle(
                                            fontFamily: 'league',
                                            fontSize: 12.sp,
                                            fontWeight: FontWeight.bold,
                                          ),
                                          textHeightBehavior:
                                              TextHeightBehavior(
                                                applyHeightToFirstAscent: false,
                                                applyHeightToLastDescent: false,
                                              ),
                                        ),
                                        Text(
                                          task.priority ?? 'N/A',
                                          style: TextStyle(
                                            fontFamily: 'league',
                                            fontSize: 12.sp,
                                          ),
                                          textHeightBehavior:
                                              TextHeightBehavior(
                                                applyHeightToFirstAscent: false,
                                                applyHeightToLastDescent: false,
                                              ),
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
                SizedBox(height: 4.h),
                Center(
                  child: SvgPicture.asset(
                    'assets/vectors/Line.svg',
                    width: 292.w,
                  ),
                ),

                SizedBox(height: 4.h),
                // SizedBox(
                //   height: 282.h,
                //   width: double.infinity,
                //   child: GoogleMap(
                //     initialCameraPosition: CameraPosition(
                //       target: LatLng(40.689247, -74.044502),
                //       zoom: 15,
                //     ),
                //     markers: {
                //       Marker(
                //         markerId: MarkerId('location'),
                //         position: LatLng(40.689247, -74.044502),
                //       ),
                //     },
                //     zoomControlsEnabled: false,
                //   ),
                // ),
                SizedBox(height: 8.h),
                Center(
                  child: SvgPicture.asset(
                    'assets/vectors/Line.svg',
                    width: 292.w,
                  ),
                ),
                SizedBox(height: 8.h),
                Center(
                  child: ShaderMask(
                    shaderCallback: (mainGradient_green).createShader,
                    blendMode: BlendMode.srcIn,
                    child: Text(
                      "Description",
                      style: TextStyle(
                        fontSize: 12.sp,
                        fontWeight: FontWeight.w900,
                        fontFamily: 'league',
                      ),
                    ),
                  ),
                ),
                Center(
                  child: Text(
                    task.description ?? 'No description provided.',
                    style: TextStyle(fontSize: 8.sp),
                  ),
                ),
                SizedBox(height: 8.h),
                Center(
                  child: SvgPicture.asset(
                    'assets/vectors/Line.svg',
                    width: 292.w,
                  ),
                ),
                SizedBox(height: 8.h),
                Center(child: Image.network(task.beforeImage!, height: 500.h)),
                SizedBox(height: 11.h),
                Center(
                  child: SvgPicture.asset(
                    'assets/vectors/Line.svg',
                    width: 292.w,
                  ),
                ),
                SizedBox(height: 8.h),
                Padding(
                  padding: EdgeInsets.only(left: 15.w),
                  child: ShaderMask(
                    shaderCallback: (mainGradient_green).createShader,
                    blendMode: BlendMode.srcIn,
                    child: Text(
                      "Reporter Info",
                      style: TextStyle(
                        fontSize: 12.sp,
                        fontWeight: FontWeight.w900,
                        fontFamily: 'league',
                      ),
                    ),
                  ),
                ),
                SizedBox(height: 8.h),
                Center(
                  child: Container(
                    width: 326.w,
                    height: 67.h,
                    decoration: BoxDecoration(
                      color: Color(0xffF9F8FF),
                      borderRadius: BorderRadius.circular(10.r),
                      border: Border.all(color: Color(0xffE6E4F0), width: 1.w),
                    ),
                    child: Padding(
                      padding: EdgeInsets.only(left: 10.w),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Row(
                            children: [
                              AlphaButton(
                                width: 142.w,
                                height: 23.h,
                                text: 'Name of the Reporter:',
                                buttonColor: 0xff7B68EE,
                                textColor: 0xff7B68EE,
                                fontsize: 12.sp,
                                radius: 33.r,
                                onTap: () {},
                              ),
                              SizedBox(width: 10.w),
                              Text(
                                task.citizenName ?? 'N/A',
                                style: TextStyle(fontSize: 12.sp),
                              ),
                            ],
                          ),
                          SizedBox(height: 8.h),

                          Row(
                            children: [
                              AlphaButton(
                                width: 109.w,
                                height: 20.h,
                                text: 'phone number:',
                                buttonColor: 0xff00B884,
                                textColor: 0xff00B884,
                                fontsize: 12.sp,
                                onTap: () {},
                                radius: 33.r,
                              ),
                              SizedBox(width: 10.w),
                              Text(
                                task.citizenPhone ?? 'N/A',
                                style: TextStyle(fontSize: 12.sp),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
                SizedBox(height: 22.h),
                Center(
                  child: state is TaskLoading
                      ? CircularProgressIndicator()
                      : AlphaButton(
                          width: 91.w,
                          height: 23.h,
                          text: 'Accept Task',
                          buttonColor: 0xff49CCF9,
                          textColor: 0xff49CCF9,
                          fontsize: 12.sp,
                          radius: 33.r,
                          onTap: () {
                            taskcubit.assignTask(
                              department:
                                  (usercubit.currentUser as EmployeeModel)
                                      .Department,
                              employeeId:
                                  (usercubit.currentUser as EmployeeModel).id
                                      .toString(),
                              taskId: task.id!.toString(),
                            );
                          },
                        ),
                ),
                SizedBox(height: 100.h),
              ],
            ),
          ),
        );
      },
    );
  }
}
