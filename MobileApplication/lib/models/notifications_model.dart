class NotificationsModel {
  final String name;
  final String location;
  final String subject;
  final String timeAgo;

  NotificationsModel({
    required this.name,
    required this.location,
    required this.subject,
    required this.timeAgo,
  });
  factory NotificationsModel.fromJson(Map<String, dynamic> json) {
    final createdAt = DateTime.parse(json['created_at']);
    final now = DateTime.now();

    final difference = now.difference(createdAt);

    String timeAgo;

    if (difference.inMinutes < 1) {
      timeAgo = 'Just now';
    } else if (difference.inHours < 1) {
      timeAgo = '${difference.inMinutes} min ago';
    } else if (difference.inDays < 1) {
      timeAgo = '${difference.inHours} h ago';
    } else {
      timeAgo = '${difference.inDays} days ago';
    }
    return NotificationsModel(
      name: json['name'] as String,
      location: json['message'].split('|')[0].trim() as String,
      subject: json['subject'] as String,
      timeAgo: timeAgo,
    );
  }
}
