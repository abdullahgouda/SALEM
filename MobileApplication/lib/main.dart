import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:salem/core/api_services.dart';
import 'package:salem/cubits/auth/auth_cubit.dart';
import 'package:salem/cubits/auth/password_cubit.dart';
import 'package:salem/cubits/nav/nav_cubit.dart';
import 'package:salem/cubits/notifications/cubit/notifications_cubit.dart';
import 'package:salem/cubits/tasks/task_cubit.dart';
import 'package:salem/repos/notifications_repo.dart';
import 'package:salem/repos/tasks_repo.dart';
import 'package:salem/repos/user_repo.dart';
import 'package:salem/view/auth/forget%20password/forget_password.dart';
import 'package:salem/view/auth/forget%20password/otp_verfiy.dart';
import 'package:salem/view/auth/forget%20password/reset_password.dart';
import 'package:salem/view/auth/login.dart';
import 'package:salem/view/auth/signup.dart';
import 'package:salem/view/auth/welcomPage.dart';
import 'package:salem/view/citizen/create_report_page.dart';
import 'package:salem/view/citizen/main_layout_citizen.dart';
import 'package:salem/view/citizen/my_reports_view.dart';
import 'package:salem/view/citizen/onboarding_screen.dart';
import 'package:salem/view/employee/main_layout_employee.dart';
import 'package:salem/view/modules/citizen_widgets/pages/success_task_page.dart';
import 'package:salem/view/employee/task_details_view.dart';
import 'package:salem/view/employee/task_progress_view.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await ApiService().loadTokens();
  final authcubit = AuthCubit(UserRepository());
  ApiService().onLogout = () {
    authcubit.forceLogout();
  };
  runApp(
    MultiBlocProvider(
      providers: [
        BlocProvider.value(value: authcubit),
        BlocProvider(create: (context) => PasswordCubit()),
        BlocProvider(create: (context) => NavCubit()),
        BlocProvider(create: (context) => TaskCubit(TaskRepo())),
        BlocProvider(create: (context) => NotificationsCubit(NotificationsRepo())),
      ],
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ScreenUtilInit(
      designSize: const Size(360, 800),
      minTextAdapt: true,
      splitScreenMode: true,
      builder: (context, child) {
        return child!;
      },
      child: MaterialApp(
        debugShowCheckedModeBanner: false,

        title: 'Salem App',
        home: Welcompage(),
        routes: {
          '/login': (context) => LoginPage(),
          '/signup': (context) => Signup(),
          '/onboarding': (context) => OnboardingScreen(),
          '/welcome': (context) => Welcompage(),
          '/mainCitizen': (context) => MainLayoutCitizen(),
          '/mainEmployee': (context) => MainLayoutEmployee(),
          '/createTask': (context) => CreateReportPage(),
          '/forgetPassword': (context) => ForgetPasswordPage(),
          '/otpVerify': (context) => OtpVerify(),
          '/resetPassword': (context) => ResetPassword(),
        },
      ),
    );
  }
}
