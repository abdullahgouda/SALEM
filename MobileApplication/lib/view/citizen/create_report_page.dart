import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:image_picker/image_picker.dart';
import 'package:intl/intl.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/cubits/tasks/task_cubit.dart';
import 'package:salem/view/modules/citizen_widgets/pages/cancel_task_page.dart';
import 'package:salem/view/modules/citizen_widgets/pages/success_task_page.dart';
import 'package:salem/view/modules/citizen_widgets/view_photo.dart';
import 'package:salem/view/modules/common/main_button.dart';
import 'package:salem/view/modules/citizen_widgets/report_options_card.dart';

class CreateReportPage extends StatelessWidget {
  CreateReportPage({super.key});
  final TextEditingController _descriptionController = TextEditingController();

  String loc_text = 'Value';
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: ShaderMask(
          shaderCallback: (mainGradient_green).createShader,
          blendMode: BlendMode.srcIn,
          child: Text(
            "Add Report",
            style: TextStyle(
              fontSize: 18.sp,
              fontWeight: FontWeight.bold,
              fontFamily: 'league',
            ),
          ),
        ),
        centerTitle: true,
      ),
      body: BlocConsumer<TaskCubit, TaskState>(
        listener: (context, state) {
          if (state is TaskError) {
            ScaffoldMessenger.of(
              context,
            ).showSnackBar(SnackBar(content: Text(state.message)));
          }

          if (state is TaskActionSuccess) {
            context.read<TaskCubit>().resetTask();
            context.read<TaskCubit>().loadCitizenTasks();
            Navigator.pushAndRemoveUntil(
              context,
              MaterialPageRoute(builder: (context) => SuccessTaskPage()),
              (route) => false,
            );
          }
        },
        builder: (context, state) {
          final cubit = context.watch<TaskCubit>();
          return SingleChildScrollView(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Padding(
                  padding: EdgeInsets.only(left: 3.w),
                  child: Text(
                    'What are you reporting?',
                    style: TextStyle(
                      fontSize: 20.sp,
                      fontFamily: 'league',
                      fontWeight: FontWeight.bold,
                      color: mainColor_navy,
                    ),
                  ),
                ),
                SizedBox(height: 12.h),

                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    ReportOptionsCard(
                      icon: 'sarf_icon',
                      title: 'Gas',
                      isSelected: cubit.isTaskTypeSelected('Gas'),
                      onTap: () {
                        context.read<TaskCubit>().selectTaskType('Gas');
                      },
                    ),
                    ReportOptionsCard(
                      icon: 'kahraba_icon',
                      title: 'Electricity',
                      isSelected: cubit.isTaskTypeSelected('Electricity'),
                      onTap: () {
                        context.read<TaskCubit>().selectTaskType('Electricity');
                      },
                    ),
                    ReportOptionsCard(
                      icon: 'toro2_icon',
                      title: 'Road',
                      isSelected: cubit.isTaskTypeSelected('Road'),
                      onTap: () {
                        context.read<TaskCubit>().selectTaskType('Road');
                      },
                    ),
                    ReportOptionsCard(
                      icon: 'other_icon',
                      title: 'Other',
                      isSelected: cubit.isTaskTypeSelected('Other'),
                      onTap: () {
                        context.read<TaskCubit>().selectTaskType('Other');
                      },
                    ),
                  ],
                ),

                SizedBox(height: 7.h),
                Padding(
                  padding: EdgeInsets.only(left: 7.w),
                  child: Text(
                    'If answering ‘Other’, please provide details in the description.',
                    style: TextStyle(
                      fontSize: 16.sp,
                      fontFamily: 'league',
                      color: Color(0XFF70707B).withValues(alpha: 0.5),
                    ),
                  ),
                ),
                SizedBox(height: 6.h),
                Padding(
                  padding: EdgeInsets.only(left: 6.w),
                  child: Text(
                    'Location',
                    style: TextStyle(
                      fontSize: 16.sp,
                      fontFamily: 'league',
                      fontWeight: FontWeight.bold,
                      color: mainColor_navy,
                    ),
                  ),
                ),
                SizedBox(height: 8.h),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    Container(
                      width: 327.w,
                      height: 40.h,
                      decoration: BoxDecoration(
                        gradient: mainGradient_green,
                        borderRadius: BorderRadius.circular(8.r),
                        border: Border.all(
                          color: Color(0XFF3F3F46),
                          width: 1.w,
                        ),
                      ),
                      child: Padding(
                        padding: EdgeInsets.only(left: 12.w, top: 8.h),
                        child: Text(
                          state is TaskLocationLoading
                              ? 'Getting Location...'
                              : (cubit.location?['address'] ?? 'Value'),
                          style: TextStyle(
                            fontSize: 16.sp,
                            fontFamily: 'league',
                            color: Colors.white,
                          ),
                        ),
                      ),
                    ),
                    GestureDetector(
                      child: state is TaskLocationLoading
                          ? SizedBox(
                              width: 21.w,
                              height: 22.h,
                              child: CircularProgressIndicator(
                                color: Colors.black,
                              ),
                            )
                          : SvgPicture.asset(
                              'assets/vectors/location_icon.svg',
                              width: 21.w,
                              height: 22.h,
                            ),
                      onTap: () {
                        context.read<TaskCubit>().getLocation();
                      },
                    ),
                  ],
                ),

                SizedBox(height: 11.h),
                Padding(
                  padding: EdgeInsets.only(left: 6.w),
                  child: Text(
                    'Description',
                    style: TextStyle(
                      fontSize: 16.sp,
                      fontFamily: 'league',
                      fontWeight: FontWeight.bold,
                      color: mainColor_navy,
                    ),
                  ),
                ),
                SizedBox(height: 8.h),
                Padding(
                  padding: EdgeInsets.symmetric(horizontal: 6.w),
                  child: TextFormField(
                    controller: _descriptionController,
                    maxLines: 2,
                    maxLength: 90,
                    decoration: InputDecoration(
                      hintText: 'Value',
                      hintStyle: TextStyle(
                        fontSize: 16.sp,
                        fontFamily: 'league',
                        color: Colors.black,
                      ),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8.r),
                        borderSide: BorderSide(
                          color: Color(0XFF3F3F46),
                          width: 1.w,
                        ),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8.r),
                        borderSide: BorderSide(
                          color: mainColor_green,
                          width: 1.w,
                        ),
                      ),
                    ),
                  ),
                ),

                Padding(
                  padding: EdgeInsets.only(left: 7.w),
                  child: Text(
                    'Picture',
                    style: TextStyle(
                      fontSize: 16.sp,
                      fontFamily: 'league',
                      fontWeight: FontWeight.bold,
                      color: Color(0XFF70707B),
                    ),
                  ),
                ),
                SizedBox(height: 8.h),
                Center(
                  child: GestureDetector(
                    onTap: () async {
                      final XFile? image = await ImagePicker().pickImage(
                        source: ImageSource.camera,
                      );

                      if (image != null) {
                        cubit.setTaskImage(
                          File(image.path),
                        );

                      }
                    },
                    child: Container(
                      width: 340.w,
                      height: 40.h,
                      decoration: BoxDecoration(
                        gradient: mainGradient_green,
                        borderRadius: BorderRadius.circular(8.r),
                        border: Border.all(
                          color: Color(0XFF3F3F46),
                          width: 1.w,
                        ),
                      ),
                      child: Padding(
                        padding: EdgeInsets.only(left: 12.w, top: 8.h),
                        child: Text(
                          'Open the camera',
                          style: TextStyle(
                            fontSize: 16.sp,
                            fontFamily: 'league',
                            color: Colors.white,
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
                BlocBuilder<TaskCubit, TaskState>(
                  builder: (context, state) {
                    final image = cubit.taskImage;

                    if (image == null) {
                      return SizedBox(height: 30.h); // مفيش زرار
                    }

                    return Padding(
                      padding: EdgeInsets.only(
                        top: 10.h,
                        bottom: 30.h,
                        left: 8.w,
                      ),
                      child: MainButton(
                        width: 80.w,
                        height: 30.h,
                        gradient: mainGradient_green,
                        text: 'View Photo',
                        font_family: 'league',
                        borderRadius: 30,
                        ontap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => ViewPhotoPage(image: image),
                            ),
                          );
                        },
                      ),
                    );
                  },
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    MainButton(
                      width: 100.w,
                      height: 40.h,
                      text: 'Cancel',
                      fontSize: 16.sp,
                      font_family: 'league',
                      color: mainColor_navy,
                      borderRadius: 9999.r,
                      ontap: () {
                        _descriptionController.clear();
                        context.read<TaskCubit>().resetTask();
                        context.read<TaskCubit>().loadCitizenTasks();
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => CancelTaskPage(
                              Resettask: () {
                                Navigator.pushNamedAndRemoveUntil(
                                  context,
                                  '/mainCitizen',
                                  (route) => false,
                                );
                              },
                            ),
                          ),
                        );
                      },
                    ),
                    SizedBox(width: 8.w),
                    BlocBuilder<TaskCubit, TaskState>(
                      builder: (context, state) {
                        return state is TaskActionLoading
                            ? CircularProgressIndicator()
                            : MainButton(
                                width: 127.w,
                                height: 40.h,
                                text: 'Submit Report',
                                fontSize: 16.sp,
                                font_family: 'league',
                                gradient: mainGradient_green,
                                borderRadius: 9999.r,
                                ontap: () {
                                  cubit.createTask({
                                    'Description': _descriptionController.text,
                                  });
                                },
                              );
                      },
                    ),
                  ],
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
