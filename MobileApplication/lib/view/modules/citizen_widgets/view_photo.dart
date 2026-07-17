import 'dart:io';
import 'package:flutter/material.dart';

class ViewPhotoPage extends StatelessWidget {
  final File image;

  const ViewPhotoPage({super.key, required this.image});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        iconTheme: IconThemeData(color: Colors.white),
        title: Text("Photo", style: TextStyle(color: Colors.white)),
      ),
      body: Center(
        child: InteractiveViewer(
          child: Image.file(image),
        ),
      ),
    );
  }
}