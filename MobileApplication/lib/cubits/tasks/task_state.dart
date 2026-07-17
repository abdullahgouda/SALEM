part of 'task_cubit.dart';

abstract class TaskState {}

class TaskInitial extends TaskState {}

class TaskLoading extends TaskState {}

class TaskActionLoading extends TaskState {}

class TaskActionSuccess extends TaskState {
 

}

class TaskLocationLoading extends TaskState {}

class TaskLocationSuccess extends TaskState {
  final Map<String, dynamic> location;

  TaskLocationSuccess(this.location);
}

class TaskLoaded extends TaskState {
  final List<TaskModel> CitizenTasks;
  final List<TaskModel> EmployeeTasks;
  final TaskModel? assignedToMe;
  final List<TaskModel> assignedToMeCompleted;

  TaskLoaded({
    required this.CitizenTasks,
    required this.EmployeeTasks,
    required this.assignedToMe,
    required this.assignedToMeCompleted,
  }); 
  }


class TaskError extends TaskState {
  final String message;

  TaskError(this.message);
}

class TaskTypeSelected extends TaskState {}
