part of 'nav_cubit.dart';

class NavState {
  final int currentIndex;

  const NavState({required this.currentIndex});

  NavState copyWith({int? currentIndex}) {
    return NavState(
      currentIndex: currentIndex ?? this.currentIndex,
    );
  }
}