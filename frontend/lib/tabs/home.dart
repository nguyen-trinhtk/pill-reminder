import 'package:flutter/material.dart';
import 'package:frontend/elements/appbar.dart';
import 'package:frontend/elements/text.dart';
import 'package:frontend/elements/medcard.dart';
import 'package:frontend/elements/button.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        title: 'Home',
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_on),
            onPressed: () {
              ScaffoldMessenger.of(
                context,
              ).showSnackBar(const SnackBar(content: Text('Notifications')));
            },
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            CustomButton(
              text: 'Take Photo',
              width: MediaQuery.of(context).size.width,
              height: MediaQuery.of(context).size.height * 0.25,
              header: true,
              fontSize: 32.0,
              onPressed:
                  () => {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Button One Pressed')),
                    ),
                  },
            ),
            CustomButton(
              text: 'Upload from Gallery',
              width: MediaQuery.of(context).size.width,
              height: MediaQuery.of(context).size.height * 0.1,
              colorType: 3,
              header: true,
              fontSize: 28.0,
              onPressed:
                  () => {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Button Two Pressed')),
                    ),
                  },
            ),
            Align(
              alignment: Alignment.centerLeft,
              child: SizedBox(
                width: MediaQuery.of(context).size.width,
                child: CustomText(
                  text: "Today's Medication",
                  header: true,
                  padding: 24,
                  textAlign: TextAlign.start,
                ),
              ),
            ),
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 24),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  spacing: 16,
                  children: [
                    MedActionCard(title:'Ibuprofen', dosage: '500mg', time: '8:00 AM'),
                    MedActionCard(title:'Paracetamol', dosage: '650mg', time: '10:00 AM'),
                    MedActionCard(title:'Aspirin', dosage: '100mg', time: '12:00 PM'),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
