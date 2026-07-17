import 'package:salem/models/base_user.dart';

class EmployeeModel extends BaseUser {
  final String Department;
  final String id;
  EmployeeModel({
    required String username,

    required String user_type,
    required this.Department, required this.id,
  }) : super(username: username, user_type: user_type);

  factory EmployeeModel.fromJson(Map<String, dynamic> json) {
    return EmployeeModel(
      username: json['Name'],
      user_type: json['User_type'],
      Department: json["Department"]['name'],
      id: json['id'].toString(),
    );
  }
}
