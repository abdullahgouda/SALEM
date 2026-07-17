import 'package:dio/dio.dart';
import 'package:salem/core/api_services.dart';
import 'package:salem/models/base_user.dart';
import 'package:salem/models/citizen_model.dart';
import 'package:salem/models/employee_model.dart';
import 'package:salem/view/auth/forget%20password/reset_password.dart';

class UserRepository {
  final ApiService _api = ApiService();

  Future<BaseUser> citizeLogin(String emailOrPhone, String password) async {
    try {
      final body = {
        "Email_or_Phone_Number": emailOrPhone,
        "Password": password,
      };

      final response = await _api.dio.post("/citizin/login/", data: body);

      final data = response.data;

      final accessToken = data["Access_Token"];
      final refreshToken = data["Refresh_Token"];

      _api.setAccessToken(accessToken);
      _api.setRefreshToken(refreshToken);
      await _api.saveTokens(accessToken, refreshToken);

      return _mapUser(data);
    } on DioException catch (e) {
      final data = e.response?.data;

      if (data is Map<String, dynamic>) {
        if (data["non_field_errors"] != null &&
            data["non_field_errors"] is List &&
            (data["non_field_errors"] as List).isNotEmpty) {
          throw Exception(data["non_field_errors"][0]);
        }

        if (data["message"] != null) {
          throw Exception(data["message"]);
        }

        for (final entry in data.entries) {
          if (entry.value is List && (entry.value as List).isNotEmpty) {
            throw Exception(entry.value[0].toString());
          }
        }
      }

      throw Exception("Login failed: ${e.message}");
    } catch (e) {
      throw Exception("Login failed: $e");
    }
  }

  Future<BaseUser> employeeLogin(String nationalId, String password) async {
    try {
      final body = {"National_id": nationalId, "Password": password};

      final response = await _api.dio.post("/employee/login/", data: body);

      final data = response.data;
      final accessToken = data["Asscess_Token"];
      final refreshToken = data["Refresh_Token"];

      _api.setAccessToken(accessToken);
      _api.setRefreshToken(refreshToken);
      await _api.saveTokens(accessToken, refreshToken);

      return _mapUser(data);
    } on DioException catch (e) {
      final data = e.response?.data;

      if (data is Map<String, dynamic>) {
        if (data["non_field_errors"] != null &&
            data["non_field_errors"] is List &&
            (data["non_field_errors"] as List).isNotEmpty) {
          throw Exception(data["non_field_errors"][0]);
        }

        if (data["message"] != null) {
          throw Exception(data["message"]);
        }

        for (final entry in data.entries) {
          if (entry.value is List && (entry.value as List).isNotEmpty) {
            throw Exception(entry.value[0].toString());
          }
        }
      }

      throw Exception("Login failed: ${e.message}");
    } catch (e) {
      throw Exception("Login failed: $e");
    }
  }

  Future<void> signup(Map<String, dynamic> userData) async {
    try {
      await _api.dio.post("/citizin/signup/", data: userData);
    } on DioException catch (e) {
      final data = e.response?.data;

      if (data is Map<String, dynamic>) {
        // لو فيه detail
        if (data["detail"] != null) {
          throw Exception(data["detail"].toString());
        }

        // لو فيه message
        if (data["message"] != null) {
          throw Exception(data["message"].toString());
        }

        // لو فيه validation errors زي email / national_id / password
        for (final entry in data.entries) {
          if (entry.value is List && (entry.value as List).isNotEmpty) {
            throw Exception(entry.value[0].toString());
          }

          if (entry.value is String) {
            throw Exception(entry.value.toString());
          }
        }
      }

      if (e.response != null) {
        throw Exception("Signup failed");
      } else {
        throw Exception("Network error: ${e.message}");
      }
    } catch (e) {
      throw Exception(e.toString().replaceFirst("Exception: ", ""));
    }
  }

  Future<void> logout() async {
    await _api.clearTokensFromStorage();
  }

  BaseUser _mapUser(Map<String, dynamic> userData) {
    if (userData["User_Type"] == "citizin") {
      return CitizenModel.fromJson(userData);
    } else {
      return EmployeeModel.fromJson(userData);
    }
  }

  Future<String> getOtp(String email) async {
    try {
      final response = await _api.dio.post(
        "/password/forgot/",
        data: {"Email": email},
      );

      return response.data['message'];
    } on DioException catch (e) {
      throw Exception(e.response?.data['message'] ?? "Something went wrong");
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  Future<String> verifyOtp(String email, String otp) async {
    try {
      final response = await _api.dio.post(
        "/password/verify-otp/",
        data: {"Email": email, "OTP": otp},
      );

      return response.data['message'];
    } on DioException catch (e) {
      if (e.response?.data['message'] == 'Invalid OTP or Email.') {
        throw Exception('Invalid OTP');
      }
      throw Exception("Something went wrong");
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  Future<String> resetPassword(
    String email,
    String password,
    String confPass,
  ) async {
    try {
      if (password != confPass) {
        throw Exception('Password Mismatch');
      }
      final response = await _api.dio.post(
        "/password/reset/",
        data: {"Email": email, "New_Password": password},
      );
      return response.data['message'];
    } on DioException catch (e) {
      if (e.response?.data['message'] ==
          'Email and New_Password are required.') {
        throw Exception('Password is required.');
      }
      throw Exception("Something went wrong");
    } catch (e) {
      throw Exception(e.toString());
    }
  }
}
