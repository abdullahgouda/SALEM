import 'dart:io';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:salem/models/tasks_model.dart';
import 'package:salem/repos/tasks_repo.dart';
import 'package:collection/collection.dart';
part 'task_state.dart';

class TaskCubit extends Cubit<TaskState> {
  TaskCubit(this.taskRepo) : super(TaskInitial());

  final TaskRepo taskRepo;
  String taskType = 'Gas';
  final List titels = ['Gas', 'Electricity', 'Road', 'Other'];
  File? taskImage;
  Map<String, dynamic>? location;
  int totalTasksToday = 0;
  int completedTasks = 0;
  int pendingTasks = 0;

  Future<void> loadCitizenTasks() async {
    emit(TaskLoading());
    try {
      emit(
        TaskLoaded(
          CitizenTasks: await taskRepo.fetchCitizentasks(),
          EmployeeTasks: [],
          assignedToMe: null,
          assignedToMeCompleted: [],
        ),
      );
    } catch (e) {
      emit(TaskError(e.toString()));
    }
  }

  Future<void> loadEmployeeTasks({
    required String department,
    required String employeeId,
  }) async {
    emit(TaskLoading());
    try {
      final allTasks = await taskRepo.fetchEmployeetasks(
        department: department,
      );

      final unassignedTasks = allTasks
          .where((task) => !task.isAssigned!)
          .toList();

      _calculateTaskStats(allTasks);
      if (allTasks.any((task) => task.assignedEmployeeId == employeeId)) {
        final assignedToMe = allTasks.firstWhereOrNull(
          (task) =>
              task.assignedEmployeeId == employeeId &&
              task.status != 'Finished',
        );

        final assignedToMeCompleted = allTasks
            .where(
              (task) =>
                  task.assignedEmployeeId == employeeId &&
                  task.status == 'Finished',
            )
            .toList();
        emit(
          TaskLoaded(
            CitizenTasks: [],
            EmployeeTasks: unassignedTasks,
            assignedToMe: assignedToMe,
            assignedToMeCompleted: assignedToMeCompleted,
          ),
        );

        return;
      }

      emit(
        TaskLoaded(
          CitizenTasks: [],
          EmployeeTasks: unassignedTasks,
          assignedToMe: null,
          assignedToMeCompleted: [],
        ),
      );
    } catch (e) {
      emit(TaskError(e.toString()));
    }
  }

  Future<void> assignTask({
    required String department,
    required String employeeId,
    required String taskId,
  }) async {
    emit(TaskLoading());

    try {
      await taskRepo.assignTask(taskId: taskId);
      await loadEmployeeTasks(department: department, employeeId: employeeId);
    } catch (e) {
      emit(TaskError(e.toString()));
    }
  }

  Future<void> taskInProgress({
    required String department,
    required String employeeId,
    required String taskId,
  }) async {
    emit(TaskLoading());

    try {
      if (location != null) {
        await taskRepo.taskInProgressWithLocation(
          taskId: taskId,
          lat: location!['latitude'],
          long: location!['longitude'],
          location: location!['address'],
        );
      } else {
        await taskRepo.taskInProgress(taskId: taskId);
      }

      await loadEmployeeTasks(department: department, employeeId: employeeId);
    } catch (e) {
      emit(TaskError(e.toString()));
    }
  }

  Future<void> taskReview(String whatWasDone, String incidenceId) async {
    if (whatWasDone.trim().isEmpty) {
      emit(TaskError("Please type what was done"));
      return;
    }

    if (taskImage == null) {
      emit(TaskError("Please take a photo"));
      return;
    }

    emit(TaskActionLoading());
    try {
      await taskRepo.taskReview({
        "imageAfterAnalysis": taskImage,
        'whatWasDone': whatWasDone,
        'incidence_id': incidenceId,
      });
      emit(TaskActionSuccess());
    } catch (e) {
      emit(TaskError(e.toString()));
    }
  }

  void _calculateTaskStats(List<TaskModel> tasks) {
    // التاريخ النهارده
    final today = DateTime.now();
    final todayDate = DateTime(today.year, today.month, today.day);

    // reset
    totalTasksToday = 0;
    completedTasks = 0;
    pendingTasks = 0;

    for (var task in tasks) {
      // لو التاسك النهارده
      if (task.date != null) {
        final taskDate = DateTime.parse(task.date!);
        final taskDateOnly = DateTime(
          taskDate.year,
          taskDate.month,
          taskDate.day,
        );

        if (taskDateOnly.isAtSameMomentAs(todayDate)) {
          totalTasksToday++;
        }
      }

      // حسب الـ status
      if (task.status?.toLowerCase() == 'completed' ||
          task.status?.toLowerCase() == 'done') {
        completedTasks++;
      } else if (task.status?.toLowerCase() == 'pending' ||
          task.status?.toLowerCase() == 'new') {
        pendingTasks++;
      }
    }
  }

  Future<void> createTask(Map<String, dynamic> taskData) async {
    if (location == null) {
      emit(TaskError("Please select location"));
      return;
    }

    if (taskData['Description'].trim().isEmpty) {
      emit(TaskError("Please enter description"));
      return;
    }

    if (taskImage == null) {
      emit(TaskError("Please take a photo"));
      return;
    }

    emit(TaskActionLoading());
    try {
      await taskRepo.createTask({
        ...taskData,
        'Department': taskType,
        "Image_Before_Analysis": taskImage,
        'Location_Name': location!['address'],
        'Longitude': location!['longitude'],
        'Latlatitude': location!['latitude'],
      });
      emit(TaskActionSuccess());
    } catch (e) {
      emit(TaskError(e.toString()));
    }
  }

  Future<void> getLocation() async {
    emit(TaskLocationLoading());

    try {
      final result = await taskRepo.getLocation();
      location = result;
      emit(TaskLocationSuccess(result));
    } catch (e) {
      emit(TaskError(e.toString()));
    }
  }

  void resetLocation({
    required String department,
    required String employeeId,
  }) async {
    location = null;
    await loadEmployeeTasks(department: department, employeeId: employeeId);
    // عشان يحصل rebuild
  }

  bool isTaskTypeSelected(String type) {
    return taskType == type;
  }

  void selectTaskType(String type) {
    emit(TaskTypeSelected());
    taskType = type;
  }

  void setTaskImage(File image) {
    taskImage = image;
    emit(TaskTypeSelected());
  }

  void resetTask() {
    taskImage = null;
    location = null;
    emit(TaskInitial());
  }
}
