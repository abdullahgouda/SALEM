import 'package:salem/models/base_user.dart';

class CitizenModel extends BaseUser {
  //final String birthDate;
  CitizenModel({
    required String username,

    required String user_type,

    //required this.birthDate,
  }) : super(username: username, user_type: user_type);

  factory CitizenModel.fromJson(Map<String, dynamic> json) {
    return CitizenModel(
      username: json['Name'],

      user_type: json['User_Type'],

      //birthDate: json['birth_date'],
    );
  }
}
