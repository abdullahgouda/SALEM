import 'dart:io';

import 'package:dio/dio.dart';
import 'package:geocoding/geocoding.dart';
import 'package:geolocator/geolocator.dart';
import 'package:salem/core/api_services.dart';
import 'package:salem/models/tasks_model.dart';

class TaskRepo {
  final ApiService _api = ApiService();

  Future<List<TaskModel>> fetchCitizentasks() async {
    try {
      final response = await _api.dio.get("/incidence/citizin/");

      List data = response.data['incidences'] as List;

      return data.map((e) => TaskModel.fromJson(e)).toList();
    } on DioException catch (e) {
      String errorMessage = "Something went wrong";

      final data = e.response?.data;

      if (data is Map) {
        if (data.containsKey('errors')) {
          final errors = data['errors'] as Map;

          errorMessage = errors.entries
              .map((entry) {
                final value = entry.value;

                if (value is List) {
                  return value.join(', ');
                }
                return value.toString();
              })
              .join('\n');
        } else if (data.containsKey('message')) {
          errorMessage = data['message'].toString();
        }
      } else {
        errorMessage = e.message ?? "Network error";
      }

      throw Exception(errorMessage);
    }
  }

  Future<List<TaskModel>> fetchEmployeetasks({
    required String department,
  }) async {
    try {
      final response = await _api.dio.get("/incidence/?Department=$department");

      List data = response.data['incidences'] as List;

      return data.map((e) => TaskModel.fromJson(e)).toList();
    } on DioException catch (e) {
      String errorMessage = "Something went wrong";

      final data = e.response?.data;

      if (data is Map) {
        if (data.containsKey('errors')) {
          final errors = data['errors'] as Map;

          errorMessage = errors.entries
              .map((entry) {
                final value = entry.value;

                if (value is List) {
                  return value.join(', ');
                }
                return value.toString();
              })
              .join('\n');
        } else if (data.containsKey('message')) {
          errorMessage = data['message'].toString();
        }
      } else {
        errorMessage = e.message ?? "Network error";
      }

      throw Exception(errorMessage);
    }
  }

  Future<void> createTask(Map<String, dynamic> taskData) async {
    try {
      final File imageFile = taskData['Image_Before_Analysis'];

      final formData = FormData.fromMap({
        "Image_Before_Analysis": await MultipartFile.fromFile(
          imageFile.path,
          filename: imageFile.path.split('/').last,
        ),
        "Description": taskData['Description'],
        "Latlatitude": double.parse(taskData['Latlatitude'].toStringAsFixed(6)),
        "Longitude": double.parse(taskData['Longitude'].toStringAsFixed(6)),
        "Location_Name": taskData['Location_Name'],
        "Department": taskData['Department'],
      });

      await _api.dio.post("/incidence/citizin/create/", data: formData);
    } on DioException catch (e) {
      String errorMessage = "Something went wrong";

      final response = e.response;

      if (response != null) {
        final data = response.data;

        if (data is Map<String, dynamic>) {
          // errors (زي validation)
          if (data['errors'] != null) {
            final errors = data['errors'] as Map;

            errorMessage = errors.entries
                .map((entry) {
                  final value = entry.value;

                  if (value is List) {
                    return value.join(', ');
                  }
                  return value.toString();
                })
                .join('\n');
          }
          // detail (Django / DRF)
          else if (data['detail'] != null) {
            errorMessage = data['detail'].toString();
          }
          // message
          else if (data['message'] != null) {
            errorMessage = data['message'].toString();
          }
          // fallback: اطبع كل حاجة
          else {
            errorMessage = data.toString();
          }
        }
        // لو رجع String
        else if (data is String) {
          errorMessage = data;
        }
      }
      // network error (no response)
      else {
        errorMessage = e.message ?? "Network error";
      }

      throw Exception(errorMessage);
    }
  }

  Future<void> assignTask({required String taskId}) async {
    try {
      final body = {"Incidence_id": taskId};

      final response = await _api.dio.post('/incidence/assign/', data: body);

      return response.data['message'];
    } on DioException catch (e) {
      throw Exception(e.response?.data['message'] ?? "Something went wrong");
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  Future<void> taskInProgress({required String taskId}) async {
    try {
      final response = await _api.dio.post('/incidence/$taskId/in-progress/');
      return response.data['message'];
    } on DioException catch (e) {
      throw Exception(e.response?.data['message'] ?? "Something went wrong");
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  Future<void> taskInProgressWithLocation({
    required String taskId,
    required double lat,
    required double long,
    required String location,
  }) async {
    try {
      final body = {"Lat": lat, "Long": long, "Location_Name": location};
      final response = await _api.dio.patch(
        '/incidence/$taskId/in-progress/',
        data: body,
      );
      return response.data['message'];
    } on DioException catch (e) {
      throw Exception(e.response?.data['message'] ?? "Something went wrong");
    } catch (e) {
      throw Exception(e.toString());
    }
  }

  Future<void> taskReview(Map<String, dynamic> taskData) async {
    try {
      final File imageFile = taskData['imageAfterAnalysis'];

      final formData = FormData.fromMap({
        "Image_After_Analysis": await MultipartFile.fromFile(
          imageFile.path,
          filename: imageFile.path.split('/').last,
        ),
        "What_Was_Done": taskData['whatWasDone'],
      });

      await _api.dio.post(
        "/incidence/${taskData['incidence_id']}/review/",
        data: formData,
      );
    } on DioException catch (e) {
      String errorMessage = "Something went wrong";

      final response = e.response;

      if (response != null) {
        final data = response.data;

        if (data is Map<String, dynamic>) {
          // errors (زي validation)
          if (data['errors'] != null) {
            final errors = data['errors'] as Map;

            errorMessage = errors.entries
                .map((entry) {
                  final value = entry.value;

                  if (value is List) {
                    return value.join(', ');
                  }
                  return value.toString();
                })
                .join('\n');
          }
          // detail (Django / DRF)
          else if (data['detail'] != null) {
            errorMessage = data['detail'].toString();
          }
          // message
          else if (data['message'] != null) {
            errorMessage = data['message'].toString();
          }
          // fallback: اطبع كل حاجة
          else {
            errorMessage = data.toString();
          }
        }
        // لو رجع String
        else if (data is String) {
          errorMessage = data;
        }
      }
      // network error (no response)
      else {
        errorMessage = e.message ?? "Network error";
      }

      throw Exception(errorMessage);
    }
  }

  Future<Map<String, dynamic>> getLocation() async {
    // check permission
    LocationPermission permission = await Geolocator.checkPermission();

    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }

    if (permission == LocationPermission.deniedForever) {
      return Future.error(
        'Location permissions are permanently denied, we cannot request permissions.',
      );
    }

    // get position
    Position position = await Geolocator.getCurrentPosition();

    double lat = position.latitude;
    double long = position.longitude;

    // get address
    List<Placemark> placemarks = await placemarkFromCoordinates(lat, long);

    Placemark place = placemarks[0];

    return {
      'latitude': lat,
      'longitude': long,
      'address': "${place.street}, ${place.locality}",
    };
  }
}
