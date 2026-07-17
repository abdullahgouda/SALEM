part of 'notifications_cubit.dart';

@immutable
sealed class NotificationsState {}

final class NotificationsInitial extends NotificationsState {}

final class NotificationsLoading extends NotificationsState {}

final class NotificationsLoaded extends NotificationsState {
  final List<NotificationsModel> notifications;
  NotificationsLoaded({required this.notifications});
}

final class NotificationsError extends NotificationsState {
  final String message;
  NotificationsError(this.message);
}
