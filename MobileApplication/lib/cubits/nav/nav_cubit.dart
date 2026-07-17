import 'package:flutter_bloc/flutter_bloc.dart';

part 'nav_state.dart';

class NavCubit extends Cubit<NavState> {
  NavCubit() : super(const NavState(currentIndex: 0));

  void changeIndex(int index) {
    emit(state.copyWith(currentIndex: index));
  }
}