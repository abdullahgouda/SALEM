import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:salem/core/constans.dart';

class CustomProgressBar extends StatelessWidget {
  final double progress;
  final int totalSteps;

  const CustomProgressBar({
    Key? key,
    required this.progress,
    required this.totalSteps,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      size: Size(double.infinity, 12.h),
      painter: ProgressBarPainter(progress: progress, totalSteps: totalSteps),
    );
  }
}

class ProgressBarPainter extends CustomPainter {
  final double progress;
  final int totalSteps;

  ProgressBarPainter({required this.progress, required this.totalSteps});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..style = PaintingStyle.fill;

    // Background (gray part)
    paint.color = Color(0xFFE0E0E0);
    final backgroundRRect = RRect.fromRectAndRadius(
      Rect.fromLTWH(0, 0, size.width, size.height),
      Radius.circular(10.r),
    );
    canvas.drawRRect(backgroundRRect, paint);

    // Progress (teal gradient)
    final progressWidth = size.width * progress; // بدل size.width
    final gradient = mainGradient_green;
    paint.shader = gradient.createShader(
      Rect.fromLTWH(0, 0, progressWidth, size.height),
    );
    final progressRRect = RRect.fromRectAndRadius(
      Rect.fromLTWH(0, 0, progressWidth, size.height),
      Radius.circular(10.r),
    );
    canvas.drawRRect(progressRRect, paint);

    // Draw step indicators

    paint.shader = null;
    final dotPadding = 42.w; // مسافة إضافية للنقط من حواف البار
    final dotsAreaWidth =
        size.width - (dotPadding * 2); // المسافة المتاحة للنقط
    final stepWidth = dotsAreaWidth / (totalSteps - 1);

    for (int i = 0; i < totalSteps; i++) {
      final x = dotPadding + (i * stepWidth);
      final isCompleted = (i / (totalSteps - 1)) <= progress;

      paint.color = isCompleted ? Colors.white : mainColor_navy;
      canvas.drawCircle(Offset(x, size.height / 2), 2.r, paint);

      // White center for completed steps
      if (isCompleted && i < totalSteps - 1) {
        paint.color = Colors.white;
        canvas.drawCircle(Offset(x, size.height / 2), 2.r, paint);
      }
    }
  }

  @override
  bool shouldRepaint(ProgressBarPainter oldDelegate) {
    return oldDelegate.progress != progress;
  }
}
