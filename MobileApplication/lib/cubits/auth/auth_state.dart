part of 'auth_cubit.dart';

abstract class AuthState {}

class AuthInitial extends AuthState {}

class AuthLoading extends AuthState {}

class AuthAuthenticated extends AuthState {
  final BaseUser user;
  AuthAuthenticated(this.user);
}

class AuthError extends AuthState {
  final String message;
  AuthError(this.message);
}

class AuthWaitingOtp extends AuthState {
  final String message;
  final String email;
  AuthWaitingOtp(this.email, this.message);
}

class AuthOtpSucess extends AuthState {
  final String message;
  final String email;
  AuthOtpSucess({required this.email, required this.message});
}

class AuthResetPasswordSucess extends AuthState {
  final String message;

  AuthResetPasswordSucess({required this.message});
}
