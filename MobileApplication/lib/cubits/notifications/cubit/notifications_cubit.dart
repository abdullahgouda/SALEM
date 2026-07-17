import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:salem/models/notifications_model.dart';
import 'package:salem/repos/notifications_repo.dart';

part 'notifications_state.dart';

class NotificationsCubit extends Cubit<NotificationsState> {
  NotificationsCubit(this.notificationsRepo) : super(NotificationsInitial());
  final NotificationsRepo notificationsRepo;
  Future<void> loadNotifications() async {
    emit(NotificationsLoading());
    try {
      List<NotificationsModel> notifications = await notificationsRepo
          .fetchNotifications();
      print(notifications[0].name);
      emit(NotificationsLoaded(notifications: notifications));
    } catch (e) {
      emit(NotificationsError(e.toString()));
    }
  }

  Future<String> requestSupport(int taskid) async {
    return await notificationsRepo.requestSupport(taskid);
  }
}
