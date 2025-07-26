import 'package:flutter/material.dart';
import 'package:frontend/elements/appbar.dart';
import 'package:frontend/elements/medcard.dart';

class MedsPage extends StatelessWidget {
  const MedsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(title: 'Medication Library'),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          physics: const BouncingScrollPhysics(),
          child: Column(
            spacing: 32,
            children: [
              MedScheduleCard(title: 'title', dosage: 'dosage', time: 'time'),
              MedScheduleCard(title: 'title', dosage: 'dosage', time: 'time'),
              MedScheduleCard(title: 'title', dosage: 'dosage', time: 'time'),
              MedScheduleCard(title: 'title', dosage: 'dosage', time: 'time')
            ],
          ),
        ),
      ),
    );
  }
}
