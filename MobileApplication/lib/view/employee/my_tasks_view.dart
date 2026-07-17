import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/cubits/tasks/task_cubit.dart';
import 'package:salem/view/modules/employee_widgets/completed_task_tile.dart';
import 'package:salem/view/modules/employee_widgets/current_task_tile.dart';

class Mytasks extends StatelessWidget {
  const Mytasks({super.key});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: SingleChildScrollView(
        child: BlocBuilder<TaskCubit, TaskState>(
          builder: (context, state) {
            if (state is TaskLoading) {
              return const Center(child: CircularProgressIndicator());
            } else if (state is TaskError) {
              return Center(child: Text(state.message));
            }
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Center(
                  child: ShaderMask(
                    shaderCallback: (mainGradient_green).createShader,
                    blendMode: BlendMode.srcIn,
                    child: Text(
                      "My Tasks",
                      style: TextStyle(
                        fontSize: 16.sp,
                        fontWeight: FontWeight.bold,
                        fontFamily: 'league',
                      ),
                    ),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.only(left: 10.w, top: 8.h, bottom: 10.h),
                  child: Text(
                    'Current Task:',
                    style: TextStyle(
                      fontSize: 20.sp,
                      fontWeight: FontWeight.w500,
                      fontFamily: 'league',
                    ),
                  ),
                ),
                if (state is TaskLoaded && state.assignedToMe != null)
                  Center(child: CurrentTaskTile(task: state.assignedToMe!)),
                if (state is TaskLoaded && state.assignedToMe == null)
                  Center(
                    child: Text(
                      'No current task assigned.',
                      style: TextStyle(
                        fontSize: 16.sp,
                        fontStyle: FontStyle.italic,
                        color: Colors.grey,
                      ),
                    ),
                  ),

                Padding(
                  padding: EdgeInsets.only(left: 10.w, top: 8.h),
                  child: Text(
                    'Completed Tasks:',
                    style: TextStyle(
                      fontSize: 20.sp,
                      fontWeight: FontWeight.w500,
                      fontFamily: 'league',
                    ),
                  ),
                ),
                if (state is TaskLoaded && state.assignedToMeCompleted != null)
                  ListView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: state.assignedToMeCompleted.length,
                    itemBuilder: (context, index) {
                      return Padding(
                        padding: EdgeInsets.symmetric(vertical: 3.h),
                        child: CompletedTaskTile(
                          task: state.assignedToMeCompleted[index],
                        ),
                      );
                    },
                  ),
                if (state is TaskLoaded && state.assignedToMeCompleted == [])
                  Center(
                    child: Text(
                      'No completed tasks yet.',
                      style: TextStyle(
                        fontSize: 16.sp,
                        fontStyle: FontStyle.italic,
                        color: Colors.grey,
                      ),
                    ),
                  ),
              ],
            );
          },
        ),
      ),
    );
  }
}
