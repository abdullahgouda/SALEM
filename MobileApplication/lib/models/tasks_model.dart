class TaskModel {
  final String? id;
  final String? type;
  final String? status;
  final String? date;
  final String? location;
  final String? priority;
  final String? beforeImage;
  final String? afterImage;
  final bool? isAssigned;
  final String? description;
  final String? citizenName;
  final String? citizenPhone;
  final String? assignedEmployeeId;
  final String? lat;
  final String? long;
  final String? whatWasDone;

  TaskModel({
    this.description,

    this.id,
    this.type,
    required this.status,
    this.date,
    this.location,

    this.priority,

    this.beforeImage,
    this.isAssigned,
    this.citizenName,
    this.citizenPhone,
    this.assignedEmployeeId,
    this.lat,
    this.long,
    this.afterImage,
    this.whatWasDone,
  });

  String get formattedDate {
    if (date == null || date!.isEmpty) return '';

    DateTime dateTime = DateTime.parse(date!);

    return "${dateTime.year}-"
        "${dateTime.month.toString().padLeft(2, '0')}-"
        "${dateTime.day.toString().padLeft(2, '0')}";
  }

  int get progressPercentage {
    if (status == null) return 0;

    switch (status) {
      case 'Assigned':
        return 25;
      case 'In_Progress':
        return 50;
      case 'Review':
        return 75;
      case 'Completed':
        return 100;
      default:
        return 0;
    }
  }

  int get progressStep {
    if (status == null) return 0;

    switch (status) {
      case 'Assigned':
        return 1;
      case 'In_Progress':
        return 2;
      case 'Review':
        return 3;
      default:
        return 0;
    }
  }

  factory TaskModel.fromJson(Map<String, dynamic> json) {
    return TaskModel(
      id: json['id']?.toString(),
      date: json['Created_At'],
      status: json['Status'],
      type: json['Department']['name'],
      beforeImage: json['Image_Before_Analysis'],
      location: json['Location_Name'],
      lat: json['Latlatitude'],
      long: json['Longitude'],
      isAssigned: json['Assigned_Employee'] != null,
      priority: json['Priority'],
      description: json['Description'],
      citizenName: json['Citizin']['Name'],
      citizenPhone: json['Citizin']['Phone_Number'],
      assignedEmployeeId: json['Assigned_Employee'] != null
          ? json['Assigned_Employee']['id'].toString()
          : null,
      afterImage: json['Image_After_Analysis'],
      whatWasDone: json['What_was_done'],
    );
  }
}
