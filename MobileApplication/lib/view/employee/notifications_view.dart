import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';
import 'package:salem/cubits/notifications/cubit/notifications_cubit.dart';
import 'package:salem/view/modules/employee_widgets/notification_tile.dart';

class Notifications extends StatelessWidget {
  const Notifications({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        AppBar(
          title: ShaderMask(
            shaderCallback: (mainGradient_green).createShader,
            blendMode: BlendMode.srcIn,
            child: Text(
              "Notification",
              style: TextStyle(
                fontSize: 24.sp,
                fontWeight: FontWeight.w900,
                fontFamily: 'league',
              ),
            ),
          ),

          centerTitle: true,
        ),

        Expanded(
          child: BlocConsumer<NotificationsCubit, NotificationsState>(
            listener: (context, state) {
              if (state is NotificationsError) {
                ScaffoldMessenger.of(
                  context,
                ).showSnackBar(SnackBar(content: Text(state.message)));
              }
            },
            builder: (context, state) {
              if (state is NotificationsLoading) {
                return Center(child: CircularProgressIndicator());
              } else if (state is NotificationsLoaded) {
                return RefreshIndicator(
                  onRefresh: () async {
                    await context
                        .read<NotificationsCubit>()
                        .loadNotifications();
                  },
                  child: ListView.builder(
                    physics: const AlwaysScrollableScrollPhysics(),
                    itemCount: state.notifications.length,
                    itemBuilder: (context, index) {
                      return NotificationTile(
                        name: state.notifications[index].name,
                        location: state.notifications[index].location,
                        timeAgo: state.notifications[index].timeAgo,
                      );
                    },
                  ),
                );
              } else {
                return Center(
                  child: Text(
                    "No notifications",
                    style: TextStyle(fontSize: 16.sp, color: Colors.grey),
                  ),
                );
              }
            },
          ),
        ),
      ],
    );
  }
}
