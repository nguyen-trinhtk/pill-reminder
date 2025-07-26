import 'package:flutter/material.dart';
import 'package:frontend/elements/appbar.dart';
import 'package:frontend/elements/text.dart';
import 'package:frontend/elements/button.dart';

class DispenserPage extends StatelessWidget {
  const DispenserPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(title: 'Dispenser'),
      body: Center(
        child: Column(
          spacing: 28,
          children: [
            const SizedBox(height: 16),
            Image(
              image: AssetImage('assets/dispenser.png'),
              height: 250
            ),
            const SizedBox(height: 40),
            CustomText(text: 'Dispenser #3201', header: true, fontSize: 28),
            CustomText(text: 'Status: Connected', fontSize: 20),
            CustomButton(text: 'Disconnect', borderRadius: 32, width: 240, header: true),
          ],
        ),
      ),
    );
  }
}
