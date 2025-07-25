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
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.center,
            spacing: 16,
            children: [
              MedCard(title: 'Ibuprofen', dosage: '500mg', time: '8:00AM'),
              MedCard(title: 'Paracetamol', dosage: '500mg', time: '12:00PM'),
              MedCard(title: 'Amoxicillin', dosage: '250mg', time: '6:00PM'),
              MedCard(title: 'Aspirin', dosage: '100mg', time: '10:00PM'),
              MedCard(title: 'Lisinopril', dosage: '10mg', time: '8:00AM'),
            ],
          ),
        ),
      ),
    );
  }
}
