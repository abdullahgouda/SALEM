import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:salem/models/base_user.dart';
import 'package:salem/repos/user_repo.dart';
import 'package:intl/intl.dart';
import 'package:salem/view/auth/forget%20password/reset_password.dart';

part 'auth_state.dart';

class AuthCubit extends Cubit<AuthState> {
  final UserRepository _repo;
  String user_type = "";
  BaseUser? currentUser;
  String role = "";

  AuthCubit(this._repo) : super(AuthInitial());

  Future<void> citizenLogin(String emailOrPhone, String password) async {
    emit(AuthLoading());

    try {
      final user = await _repo.citizeLogin(emailOrPhone, password);
      currentUser = user;
      emit(AuthAuthenticated(user));
    } catch (e) {
      emit(AuthError(e.toString().replaceFirst("Exception: ", "")));
    }
  }

  Future<void> employeeLogin(String nationalId, String password) async {
    emit(AuthLoading());

    try {
      final user = await _repo.employeeLogin(nationalId, password);
      currentUser = user;
      emit(AuthAuthenticated(user));
    } catch (e) {
      emit(AuthError(e.toString().replaceFirst("Exception: ", "")));
    }
  }

  Future<void> signup(Map<String, dynamic> userData) async {
    emit(AuthLoading());

    try {
      await _repo.signup(userData);
      emit(AuthInitial());
    } catch (e) {
      emit(AuthError(e.toString().replaceFirst("Exception: ", "")));
    }
  }

  Future<void> logout() async {
    emit(AuthLoading());
    await _repo.logout();
    user_type = "";
    currentUser = null;
    emit(AuthInitial());
  }

  void setUserType_citizen() {
    user_type = 'citizen';
    emit(AuthInitial());
  }

  void setUserType_employee() {
    user_type = 'employee';
    emit(AuthInitial());
  }

  void resetUserType() {
    user_type = '';
    emit(AuthInitial());
  }

  void forceLogout() {
    emit(AuthLoading());
    user_type = "";
    currentUser = null;
    emit(AuthInitial());
  }

  String formatBirthDate(DateTime date) {
    return DateFormat('yyyy-MM-dd').format(date);
  }

  Future<void> getOtp(String email) async {
    try {
      emit(AuthLoading());
      String message = await _repo.getOtp(email);
      emit(AuthWaitingOtp(email, message));
    } catch (e) {
      emit(AuthError(e.toString().replaceFirst("Exception: ", "")));
    }
  }

  Future<void> verifyOtp(String email, String otp) async {
    try {
      emit(AuthLoading());
      String message = await _repo.verifyOtp(email, otp);
      emit(AuthOtpSucess(message: message, email: email));
    } catch (e) {
      emit(AuthError(e.toString().replaceFirst("Exception: ", "")));
    }
  }

  Future<void> resetPassword(
    String email,
    String password,
    String confPass,
  ) async {
    try {
      emit(AuthLoading());
      String message = await _repo.resetPassword(email, password, confPass);
      emit(AuthResetPasswordSucess(message: message));
    } catch (e) {
      emit(AuthError(e.toString().replaceFirst("Exception: ", "")));
    }
  }
}
