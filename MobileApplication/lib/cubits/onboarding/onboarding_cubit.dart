import 'package:flutter_bloc/flutter_bloc.dart';

class OnboardingState {
  final int currentPage;
  final bool isLastPage;

  OnboardingState({required this.currentPage, required this.isLastPage});
}

class OnboardingCubit extends Cubit<OnboardingState> {
  OnboardingCubit() : super(OnboardingState(currentPage: 0, isLastPage: false));

  void changePage(int index) {
    emit(OnboardingState(currentPage: index, isLastPage: index == 2));
  }
}
