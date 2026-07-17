import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/cubits/onboarding/onboarding_cubit.dart';
import 'package:salem/view/modules/citizen_widgets/onboarding_page.dart';
import 'package:smooth_page_indicator/smooth_page_indicator.dart';

class OnboardingScreen extends StatelessWidget {
  OnboardingScreen({super.key});

  final PageController _controller = PageController();

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => OnboardingCubit(),
      child: Scaffold(
        body: BlocBuilder<OnboardingCubit, OnboardingState>(
          builder: (context, state) {
            final cubit = context.read<OnboardingCubit>();

            return Stack(
              children: [
                Container(
                  decoration: const BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topRight,
                      end: Alignment.bottomLeft,
                      colors: [Color(0xFF00816F), Color(0xFF2DDBC9)],
                    ),
                  ),
                  child: Opacity(
                    opacity: 0.6,
                    child: SvgPicture.asset(
                      'assets/vectors/Vector.svg',
                      width: double.infinity,
                      height: double.infinity,
                      fit: BoxFit.cover,
                    ),
                  ),
                ),
                PageView(
                  controller: _controller,
                  onPageChanged: cubit.changePage,
                  children: const [
                    OnboardPage(
                      image: "assets/vectors/onboarding1.png",
                      title: 'Register your report in seconds',
                    ),
                    OnboardPage(
                      image: "assets/vectors/onboarding2.png",
                      title: 'Track your report in real-time',
                    ),
                    OnboardPage(
                      image: "assets/vectors/onboarding3.png",
                      title: 'Be part of a better city',
                    ),
                  ],
                ),

                /// Skip
                Positioned(
                  top: 76.h,
                  left: 316.w,
                  child: GestureDetector(
                    onTap: () {
                      Navigator.pushNamedAndRemoveUntil(
                        context,
                        "/mainCitizen",
                        (route) => false,
                      );
                    },
                    child: Text(
                      "Skip",
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 14.sp,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ),

                /// Bottom
                Positioned(
                  top: 705.h,
                  left: 32.w,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      SmoothPageIndicator(
                        controller: _controller,
                        count: 3,
                        effect: ExpandingDotsEffect(
                          dotHeight: 4.h,
                          dotWidth: 4.w,
                          expansionFactor: 5,
                          spacing: 4.h,
                          dotColor: Colors.white54,
                          activeDotColor: Colors.white,
                        ),
                      ),
                      SizedBox(width: 208.w),
                      FloatingActionButton(
                        shape: CircleBorder(),
                        elevation: 0,
                        backgroundColor: Colors.white,
                        onPressed: () {
                          if (state.isLastPage) {
                            Navigator.pushNamedAndRemoveUntil(
                              context,
                              "/mainCitizen",
                              (route) => false,
                            );
                          } else {
                            _controller.nextPage(
                              duration: const Duration(milliseconds: 500),
                              curve: Curves.easeInOut,
                            );
                          }
                        },
                        child: Image.asset("assets/vectors/right_arrow.png"),
                      ),
                    ],
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
