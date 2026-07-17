import 'package:salem/core/api_services.dart';
import 'package:salem/models/notifications_model.dart';

class NotificationsRepo {
  final ApiService _api = ApiService();

  Future<List<NotificationsModel>> fetchNotifications() async {
    try {
      final response = await _api.dio.get('/notifications/');
      List data = response.data as List;

      return data.map((e) => NotificationsModel.fromJson(e)).toList();
    } catch (e) {
      throw Exception('Error fetching notifications: $e');
    }
  }

  Future<String> requestSupport(int taskid) async {
    final response = await _api.dio.post(
      '/incidence/notify-operators/',
      data: {'Incidence_id': taskid},
    );
    return response.data['message'] as String;
  }
}
