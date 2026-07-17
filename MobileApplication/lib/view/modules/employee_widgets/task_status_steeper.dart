import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:salem/core/constans.dart';

class TaskStatusStepper extends StatelessWidget {
  final int currentStep; // من 0 لـ 4
  final List<String> stepTitles;

  const TaskStatusStepper({
    Key? key,
    required this.currentStep,
    this.stepTitles = const [
      'Reported',
      'Assigned',
      'In Progress',
      'Review',
      'Resolved',
    ],
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.start,
      children: [
        SizedBox(height: 8.h),
        CustomPaint(
          size: Size(double.infinity, 40.h),
          painter: StepperPainter(
            currentStep: currentStep,
            totalSteps: stepTitles.length,
          ),
        ),

        // التيتلات
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: List.generate(
            stepTitles.length,
            (index) => Padding(
              padding: EdgeInsets.only(left: index == 0 ? 0 : 12.w),
              child: Text(
                stepTitles[index],
                style: TextStyle(
                  fontSize: 10.sp,
                  color: Color(0xFF6F6F6F),
                  fontWeight: FontWeight.w500,
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }
}

class StepperPainter extends CustomPainter {
  final int currentStep;
  final int totalSteps;

  StepperPainter({required this.currentStep, required this.totalSteps});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..style = PaintingStyle.fill
      ..strokeCap = StrokeCap.round;

    final dotPadding = 60.w;
    final dotsAreaWidth = size.width - (dotPadding * 2);
    final stepWidth = dotsAreaWidth / (totalSteps - 1);

    // رسم الخطوط بين النقط
    for (int i = 0; i < totalSteps - 1; i++) {
      final x1 = dotPadding + (i * stepWidth);
      final x2 = dotPadding + ((i + 1) * stepWidth);

      final isCompleted = i < currentStep;

      final gradient = isCompleted
          ? mainGradient_green
          : LinearGradient(colors: [Color(0xFFC6C6C6), Color(0xFFC6C6C6)]);

      paint.shader = gradient.createShader(
        Rect.fromPoints(
          Offset(x1, size.height / 2),
          Offset(x2, size.height / 2),
        ),
      );

      paint.strokeWidth = 1;
      paint.style = PaintingStyle.stroke;

      canvas.drawLine(
        Offset(x1, size.height / 2),
        Offset(x2, size.height / 2),
        paint,
      );
    }

    paint.style = PaintingStyle.fill;

    // رسم النقط
    for (int i = 0; i < totalSteps; i++) {
      final x = dotPadding + (i * stepWidth);
      final isCompleted = i < currentStep;
      final isCurrent = i == currentStep;

      if (isCompleted) {
        // خطوة مكتملة: دايرة خضرا مع علامة صح
        paint.shader = mainGradient_green.createShader(
          Rect.fromCircle(center: Offset(x, size.height / 2), radius: 12.r),
        );
        canvas.drawCircle(Offset(x, size.height / 2), 12.r, paint);
        paint.shader = null;

        // علامة صح بيضا
        paint.color = Colors.white;
        paint.style = PaintingStyle.stroke;
        paint.strokeWidth = 2;

        final checkPath = Path();
        checkPath.moveTo(x - 4, size.height / 2);
        checkPath.lineTo(x - 1, size.height / 2 + 3);
        checkPath.lineTo(x + 4, size.height / 2 - 3);
        canvas.drawPath(checkPath, paint);

        paint.style = PaintingStyle.fill;
      } else if (isCurrent) {
        // الخطوة الحالية: دايرة بيضا مع border أخضر + play icon
        paint.color = Colors.white;
        canvas.drawCircle(Offset(x, size.height / 2), 12.r, paint);

        paint.color = Color(0xFF00897B);
        paint.style = PaintingStyle.stroke;
        paint.strokeWidth = 1.5;
        canvas.drawCircle(Offset(x, size.height / 2), 12.r, paint);

        paint.shader = mainGradient_green.createShader(
          Rect.fromCircle(center: Offset(x, size.height / 2), radius: 12.r),
        );
        paint.style = PaintingStyle.fill;
        paint.strokeWidth = 1.5;
        canvas.drawCircle(Offset(x, size.height / 2), 4.r, paint);
        paint.shader = null;
        paint.style = PaintingStyle.fill;
      } else {
        // خطوة لم تكتمل: دايرة رمادي فاضية
        paint.color = Colors.white;
        canvas.drawCircle(Offset(x, size.height / 2), 12.r, paint);

        paint.color = Colors.grey[400]!;
        paint.style = PaintingStyle.stroke;
        paint.strokeWidth = 2;
        canvas.drawCircle(Offset(x, size.height / 2), 12.r, paint);

        paint.style = PaintingStyle.fill;
      }
    }
  }

  @override
  bool shouldRepaint(StepperPainter oldDelegate) {
    return oldDelegate.currentStep != currentStep;
  }
}
