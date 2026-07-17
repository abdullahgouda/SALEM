import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:image_picker/image_picker.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/cubits/auth/auth_cubit.dart';
import 'package:salem/cubits/notifications/cubit/notifications_cubit.dart';
import 'package:salem/cubits/tasks/task_cubit.dart';
import 'package:salem/models/employee_model.dart';
import 'package:salem/models/tasks_model.dart';
import 'package:salem/view/modules/common/alpha_button.dart';
import 'package:salem/view/modules/common/main_button.dart';
import 'package:salem/view/modules/employee_widgets/task_status_steeper.dart';

class TaskProgressView extends StatefulWidget {
  const TaskProgressView({super.key, required this.taskId});
  final String taskId;

  @override
  State<TaskProgressView> createState() => _TaskProgressViewState();
}

class _TaskProgressViewState extends State<TaskProgressView> {
  bool isLoadingLocation = false;
  final TextEditingController whatWasDoneController = TextEditingController();
  @override
  Widget build(BuildContext context) {
    return BlocConsumer<TaskCubit, TaskState>(
      listener: (context, state) {
        if (state is TaskError) {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text(state.message)));
          context.read<TaskCubit>().loadEmployeeTasks(
            department: (context.read<AuthCubit>().currentUser as EmployeeModel)
                .Department,
            employeeId: (context.read<AuthCubit>().currentUser as EmployeeModel)
                .id
                .toString(),
          );
        }

        if (state is TaskLocationLoading) {
          setState(() {
            isLoadingLocation = true;
          });
        }
        if (state is TaskLocationSuccess || state is TaskError) {
          setState(() {
            isLoadingLocation = false;
          });
        }
      },
      builder: (context, state) {
        final usercubit = context.read<AuthCubit>();
        final taskcubit = context.read<TaskCubit>();
        TaskModel? task;
        final image = taskcubit.taskImage;

        if (state is TaskLoaded && state.assignedToMe?.id == widget.taskId) {
          task = state.assignedToMe;
        }

        if (task == null) {
          return Scaffold(
            appBar: AppBar(
              centerTitle: true,
              title: ShaderMask(
                shaderCallback: (mainGradient_green).createShader,
                blendMode: BlendMode.srcIn,
                child: Text(
                  "Loading...",
                  style: TextStyle(
                    fontSize: 24.sp,
                    fontWeight: FontWeight.w600,
                    fontFamily: 'league',
                  ),
                ),
              ),
            ),

            body: Center(child: CircularProgressIndicator()),
          );
        }
        String displayLocation =
            taskcubit.location?['address'] ?? task.location ?? '';

        return Scaffold(
          appBar: AppBar(
            title: ShaderMask(
              shaderCallback: (mainGradient_green).createShader,
              blendMode: BlendMode.srcIn,
              child: Text(
                "Task Id #${task.id}",
                style: TextStyle(
                  fontSize: 24.sp,
                  fontWeight: FontWeight.w600,
                  fontFamily: 'league',
                ),
              ),
            ),
            centerTitle: true,
            leading: Center(
              child: SizedBox(
                width: 16.w,
                height: 16.h,
                child: GestureDetector(
                  child: SvgPicture.asset(
                    'assets/vectors/long_back_arrow.svg',

                    fit: BoxFit.contain,
                  ),
                  onTap: () => Navigator.pop(context),
                ),
              ),
            ),
          ),
          body: SingleChildScrollView(
            child: Padding(
              padding: EdgeInsets.symmetric(horizontal: 8.w),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    height: 60.h,
                    decoration: BoxDecoration(
                      gradient: mainGradient_green,
                      borderRadius: BorderRadius.circular(17.r),
                    ),
                    child: Center(
                      child: Container(
                        width: 333.06.w,
                        height: 41.91.h,
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(13.r),
                          color: Colors.white,
                        ),
                        child: Padding(
                          padding: EdgeInsets.only(left: 19.48.w, top: 6.37.h),
                          child: Column(
                            children: [
                              Row(
                                children: [
                                  Text(
                                    'Task: ',
                                    style: TextStyle(
                                      fontSize: 12.sp,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                                  Text(
                                    task.description!,
                                    style: TextStyle(
                                      fontSize: 12.sp,
                                      fontWeight: FontWeight.w400,
                                    ),
                                  ),
                                ],
                              ),
                              Row(
                                children: [
                                  Text(
                                    'Step: ',
                                    style: TextStyle(
                                      fontSize: 12.sp,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                                  Text(
                                    'Step ${task.progressStep.toString()} of 5',
                                    style: TextStyle(
                                      fontSize: 12.sp,
                                      fontWeight: FontWeight.w400,
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                  SizedBox(height: 11.h),
                  Container(
                    width: 344.w,
                    height: 80.h,
                    decoration: BoxDecoration(
                      color: Color(0xFFE0E0E0),
                      borderRadius: BorderRadius.circular(8.r),
                    ),
                    child: Center(
                      child: TaskStatusStepper(currentStep: task.progressStep),
                    ),
                  ),
                  SizedBox(height: 22.h),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        '📝 Required Inputs:',
                        style: TextStyle(
                          fontSize: 12.sp,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                      task.progressStep > 1
                          ? Container()
                          : AlphaButton(
                              width: 100.w,
                              height: 23.h,
                              text: 'Location reset',
                              buttonColor: 0xffFF0000,
                              textColor: 0xffFF0000,
                              fontsize: 12.sp,
                              radius: 33.r,
                              onTap: () {
                                taskcubit.resetLocation(
                                  department:
                                      (usercubit.currentUser as EmployeeModel)
                                          .Department,
                                  employeeId:
                                      (usercubit.currentUser as EmployeeModel)
                                          .id
                                          .toString(),
                                );
                              },
                            ),
                    ],
                  ),
                  SizedBox(height: 11.h),
                  Center(
                    child: Container(
                      width: 319.w,

                      decoration: BoxDecoration(
                        color: Color(0xFFF9F8FF),
                        borderRadius: BorderRadius.circular(10.r),
                        border: Border.all(
                          color: Color(0xFFE6E4F0),
                          width: 1.w,
                        ),
                      ),
                      child: Padding(
                        padding: EdgeInsets.only(top: 10.h, left: 13.w),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                ShaderMask(
                                  shaderCallback:
                                      (mainGradient_green).createShader,
                                  blendMode: BlendMode.srcIn,
                                  child: Text(
                                    task.progressStep > 1
                                        ? "Location: "
                                        : "Location Confirmation: ",
                                    style: TextStyle(
                                      fontSize: 12.sp,
                                      fontWeight: FontWeight.w400,
                                      fontFamily: 'league',
                                    ),
                                  ),
                                ),
                                Expanded(
                                  child: Text(
                                    displayLocation,
                                    overflow: TextOverflow.ellipsis,
                                    style: TextStyle(
                                      fontSize: 11.sp,
                                      fontWeight: FontWeight.w400,
                                      fontFamily: 'league',
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            task.progressStep > 1
                                ? Container()
                                : Padding(
                                    padding: EdgeInsets.only(
                                      left: 53.w,
                                      top: 5.h,
                                    ),
                                    child: state is TaskLoading
                                        ? Padding(
                                            padding: EdgeInsetsGeometry.only(
                                              left: 70.w,
                                            ),
                                            child: CircularProgressIndicator(),
                                          )
                                        : Row(
                                            children: [
                                              AlphaButton(
                                                width: 117.w,
                                                height: 23.h,
                                                text: 'Accept location',
                                                buttonColor: 0xFF7B68EE,
                                                textColor: 0xFF7B68EE,
                                                fontsize: 12.sp,
                                                radius: 33.r,
                                                onTap: () {
                                                  taskcubit.taskInProgress(
                                                    department:
                                                        (usercubit.currentUser
                                                                as EmployeeModel)
                                                            .Department,
                                                    employeeId:
                                                        (usercubit.currentUser
                                                                as EmployeeModel)
                                                            .id
                                                            .toString(),
                                                    taskId: widget.taskId,
                                                  );
                                                },
                                              ),
                                              SizedBox(width: 38.w),
                                              isLoadingLocation
                                                  ? CircularProgressIndicator()
                                                  : AlphaButton(
                                                      width: 44.w,
                                                      height: 23.h,
                                                      text: 'Edit',
                                                      buttonColor: 0xFF00B884,
                                                      textColor: 0xFF00B884,
                                                      fontsize: 12.sp,
                                                      radius: 33.r,
                                                      onTap: () async {
                                                        await taskcubit
                                                            .getLocation();
                                                        await taskcubit.loadEmployeeTasks(
                                                          department:
                                                              (usercubit.currentUser
                                                                      as EmployeeModel)
                                                                  .Department,
                                                          employeeId:
                                                              (usercubit.currentUser
                                                                      as EmployeeModel)
                                                                  .id
                                                                  .toString(),
                                                        );
                                                      },
                                                    ),
                                            ],
                                          ),
                                  ),
                            SizedBox(height: 5.h),
                          ],
                        ),
                      ),
                    ),
                  ),
                  task.progressStep == 2
                      ? Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            SizedBox(height: 8.h),
                            Center(
                              child: Container(
                                width: 319.w,

                                decoration: BoxDecoration(
                                  color: Color(0xFFF9F8FF),
                                  borderRadius: BorderRadius.circular(10.r),
                                  border: Border.all(
                                    color: Color(0xFFE6E4F0),
                                    width: 1.w,
                                  ),
                                ),
                                child: Padding(
                                  padding: EdgeInsets.only(
                                    top: 10.h,
                                    left: 13.w,
                                  ),
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      ShaderMask(
                                        shaderCallback:
                                            (mainGradient_green).createShader,
                                        blendMode: BlendMode.srcIn,
                                        child: Text(
                                          "What was done?",
                                          style: TextStyle(
                                            fontSize: 12.sp,
                                            fontWeight: FontWeight.w400,
                                            fontFamily: 'league',
                                          ),
                                        ),
                                      ),
                                      Padding(
                                        padding: EdgeInsets.only(top: 5.h),
                                        child: Container(
                                          width: 295.w,

                                          decoration: BoxDecoration(
                                            color: Color(
                                              0xFF00B884,
                                            ).withValues(alpha: 0.3),
                                            borderRadius: BorderRadius.circular(
                                              33.r,
                                            ),
                                          ),
                                          child: Padding(
                                            padding: EdgeInsetsGeometry.only(
                                              left: 12.w,
                                              bottom: 2.h,
                                              right: 12.w,
                                            ),
                                            child: TextFormField(
                                              controller: whatWasDoneController,
                                              maxLines: 1,
                                              decoration: InputDecoration(
                                                hintText:
                                                    'input field(Briefly write down the actions taken...) ',
                                                hintStyle: TextStyle(
                                                  color: Color(0xFF00B884),
                                                  fontSize: 12.sp,
                                                  fontFamily: 'league',
                                                ),

                                                contentPadding: EdgeInsets.zero,
                                                isDense: true,
                                                border: InputBorder.none,
                                              ),
                                            ),
                                          ),
                                        ),
                                      ),
                                      SizedBox(height: 8.h),
                                    ],
                                  ),
                                ),
                              ),
                            ),
                            SizedBox(height: 22.h),
                            Text(
                              'Upload After Photos:',
                              style: TextStyle(
                                fontSize: 12.sp,
                                fontWeight: FontWeight.w700,
                              ),
                            ),
                            SizedBox(height: 11.h),

                            Center(
                              child: Container(
                                width: 319.w,
                                height: 97,
                                decoration: BoxDecoration(
                                  color: Color(0xffF9F8FF),
                                  border: Border.all(
                                    color: Color(0xffE6E4F0),
                                    width: 1.w,
                                  ),
                                ),
                                child: Center(
                                  child: AlphaButton(
                                    width: 295.w,
                                    height: 50.h,

                                    text: image == null
                                        ? 'Open Camera  (Take photo showing the completed work)'
                                        : 'Change Photo',
                                    buttonColor: 0xFF00B884,
                                    textColor: 0xFF00B884,
                                    fontsize: 12.sp,
                                    radius: 15.r,
                                    onTap: () async {
                                      final XFile? image = await ImagePicker()
                                          .pickImage(
                                            source: ImageSource.camera,
                                          );

                                      if (image != null) {
                                        taskcubit.setTaskImage(
                                          File(image.path),
                                        );
                                      }
                                      await taskcubit.loadEmployeeTasks(
                                        department:
                                            (usercubit.currentUser
                                                    as EmployeeModel)
                                                .Department,
                                        employeeId:
                                            (usercubit.currentUser
                                                    as EmployeeModel)
                                                .id
                                                .toString(),
                                      );
                                    },
                                  ),
                                ),
                              ),
                            ),
                          ],
                        )
                      : Container(),
                  image == null
                      ? task.afterImage == null
                            ? Container()
                            : Column(
                                children: [
                                  SizedBox(height: 11.h),
                                  Center(
                                    child: Image.network(
                                      task.afterImage!,
                                      fit: BoxFit.cover,
                                    ),
                                  ),
                                  SizedBox(height: 50.h),
                                ],
                              )
                      : Padding(
                          padding: EdgeInsets.only(top: 11.h, bottom: 50.h),
                          child: Center(
                            child: Image.file(image, fit: BoxFit.cover),
                          ),
                        ),
                  task.progressStep != 2
                      ? Container()
                      : Column(
                          children: [
                            SizedBox(height: 80.h),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                MainButton(
                                  text: 'Submit Resolution',
                                  ontap: () async {
                                    await taskcubit.taskReview(
                                      whatWasDoneController.text,
                                      widget.taskId,
                                    );
                                    await taskcubit.loadEmployeeTasks(
                                      department:
                                          (usercubit.currentUser
                                                  as EmployeeModel)
                                              .Department,
                                      employeeId:
                                          (usercubit.currentUser
                                                  as EmployeeModel)
                                              .id
                                              .toString(),
                                    );
                                  },
                                  font_family: 'league',
                                  width: 159.w,
                                  height: 30.h,
                                  fontSize: 18.sp,
                                  gradient: mainGradient_green,
                                  borderRadius: 30.r,
                                ),
                                SizedBox(width: 32.w),
                                MainButton(
                                  text: 'Request Support',
                                  ontap: () async {
                                    try {
                                      final msg = await context
                                          .read<NotificationsCubit>()
                                          .requestSupport(
                                            int.parse(widget.taskId),
                                          );

                                      ScaffoldMessenger.of(
                                        context,
                                      ).showSnackBar(
                                        SnackBar(content: Text(msg)),
                                      );
                                    } catch (e) {
                                      ScaffoldMessenger.of(
                                        context,
                                      ).showSnackBar(
                                        SnackBar(content: Text(e.toString())),
                                      );
                                    }
                                  },
                                  font_family: 'league',
                                  width: 139.42.w,
                                  height: 30.h,
                                  fontSize: 16.sp,
                                  color: mainColor_navy,
                                  borderRadius: 30.r,
                                ),
                              ],
                            ),
                            SizedBox(height: 50.h),
                          ],
                        ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}
