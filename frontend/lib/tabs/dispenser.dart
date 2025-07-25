import 'package:flutter/material.dart';
import 'package:frontend/elements/appbar.dart';
import 'package:frontend/elements/text.dart';

class DispenserPage extends StatelessWidget {
  const DispenserPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        title: 'Dispenser',
      ),
      body: Center(
        child: CustomText(text:'Dispenser Page')
      ),
    );
  }
}

