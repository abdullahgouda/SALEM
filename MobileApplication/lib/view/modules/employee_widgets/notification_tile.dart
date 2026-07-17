import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:flutter_svg/svg.dart';
import 'package:salem/core/constans.dart';

class NotificationTile extends StatelessWidget {
  const NotificationTile({
    super.key,
    required this.name,
    required this.location,
    required this.timeAgo,
  });
  final String name;
  final String location;
  final String timeAgo;
  @override
  Widget build(BuildContext context) {
    return Container(
      width: 360.w,
      padding: EdgeInsets.symmetric(vertical: 12.h),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          SizedBox(width: 30.w),
          Container(
            width: 45.w,
            height: 45.h,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              gradient: mainGradient_green,
            ),
            child: Center(
              child: SvgPicture.asset('assets/vectors/dayra_laz.svg'),
            ),
          ),
          SizedBox(width: 22.w),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'System Reminder Engine',
                      style: TextStyle(
                        fontSize: 16.sp,
                        fontWeight: FontWeight.w500,
                        fontFamily: 'league',
                      ),
                    ),
                    Text(
                      timeAgo,
                      textHeightBehavior: TextHeightBehavior(
                        applyHeightToFirstAscent: false,
                        applyHeightToLastDescent: false,
                      ),
                      style: TextStyle(
                        color: Color(0xffA34231),
                        fontSize: 12.sp,
                        fontWeight: FontWeight.w400,
                        fontFamily: 'league',
                      ),
                    ),
                  ],
                ),
                SizedBox(height: 4.h),
                Text(
                  '$name submitted a support request for a Gas Incident.\nLocation: $location',
                  maxLines: 3,
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(
                    fontSize: 14.sp,
                    fontWeight: FontWeight.w400,
                    fontFamily: 'league',
                  ),
                ),
              ],
            ),
          ),
          SizedBox(width: 30.w),
        ],
      ),
    );
  }
}
