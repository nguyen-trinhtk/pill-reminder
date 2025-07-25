import 'package:flutter/material.dart';
import 'package:frontend/elements/appbar.dart';
import 'package:frontend/elements/text.dart';

class AddPage extends StatelessWidget {
  const AddPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        title: 'Add New',
      ),
      body: Center(
        child: CustomText(text:'Just a temp/middle page')
      ),
    );
  }
}

