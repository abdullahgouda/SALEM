
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:salem/cubits/auth/auth_cubit.dart';
import 'package:salem/cubits/nav/nav_cubit.dart';
import 'package:salem/view/employee/notifications_view.dart';
import 'package:salem/view/modules/common/pages/profile_view.dart';
import 'package:salem/view/employee/home_view_employee.dart';
import 'package:salem/view/employee/my_tasks_view.dart';
import 'package:salem/view/modules/common/nav_bar.dart';

class MainLayoutEmployee extends StatelessWidget {
  const MainLayoutEmployee({super.key});

  @override
  Widget build(BuildContext context) {
    final List<Widget> pages = const [
      EmployeeHome(),
      Mytasks(),
      Notifications(),
      Profile(),
    ];

    return BlocProvider(
      create: (context) => NavCubit(),
      child: BlocListener<AuthCubit, AuthState>(
        listener: (context, state) {
          // لو عندك AuthInitial أو AuthUnauthenticated استخدم اللي موجود عندك
          if (state is AuthInitial) {
            Navigator.pushNamedAndRemoveUntil(
              context,
              '/welcome',
              (route) => false,
            );
          }

          if (state is AuthError) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text(state.message),
              ),
            );
          }
        },
        child: BlocBuilder<NavCubit, NavState>(
          builder: (context, state) {
            final cubit = context.read<NavCubit>();

            return Scaffold(
              backgroundColor: const Color(0xffF5F5F5),
              body: IndexedStack(
                index: state.currentIndex,
                children: pages,
              ),
              bottomNavigationBar: MainBottomNavBar(
                isEmployee: true,
                currentIndex: state.currentIndex,
                onTap: (index) {
                  cubit.changeIndex(index);
                },
              ),
            );
          },
        ),
      ),
    );
  }
}