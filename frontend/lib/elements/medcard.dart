import 'package:flutter/material.dart';
import 'package:frontend/elements/container.dart';
import 'package:frontend/elements/text.dart';
import 'package:frontend/elements/button.dart';
import 'package:frontend/elements/weekday_picker.dart';

class MedActionCard extends StatelessWidget {
  final String title;
  final String dosage;
  final String time;
  // final String imageUrl;

  const MedActionCard({
    Key? key,
    required this.title,
    required this.dosage,
    required this.time,
    // required this.imageUrl,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return CustomContainer(
      width: 300,
      borderRadius: 24,
      child: Column(
        spacing: 16,
        children: [
          Row(
            spacing: 16,
            children: [
              CustomContainer(
                width: 100,
                height: 74,
                colorType: 2,
                child: const Icon(Icons.photo, size: 32, color: Colors.grey),
              ),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    CustomText(text: title, header: true),
                    CustomText(text: dosage, fontSize: 16),
                    CustomText(text: time, fontSize: 16),
                  ],
                ),
              ),
            ],
          ),
          Row(
            children: [
              Expanded(
                child: CustomButton(
                  text: '✗ Skip',
                  header: true,
                  fontSize: 18,
                  colorType: 2,
                  borderRadius: 32,
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: CustomButton(
                  text: '✓ Done',
                  header: true,
                  fontSize: 18,
                  colorType: 3,
                  borderRadius: 32,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class MedScheduleCard extends StatelessWidget {
  final String title;
  final String dosage;
  final String time;
  // final String imageUrl;
  const MedScheduleCard({
    Key? key,
    required this.title,
    required this.dosage,
    required this.time,
    // required this.imageUrl,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return CustomContainer(
      width: 300,
      borderRadius: 24,
      child: Column(
        spacing: 16,
        children: [
          Row(
            spacing: 16,
            children: [
              CustomContainer(
                width: 100,
                height: 74,
                colorType: 2,
                child: const Icon(Icons.photo, size: 32, color: Colors.grey),
              ),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    CustomText(text: title, header: true),
                    CustomText(text: dosage, fontSize: 16),
                    CustomText(text: time, fontSize: 16),
                  ],
                ),
              ),
            ],
          ),
          WeekdayPicker(
            selectable: false,
            initialSelected: ['Mon', 'Wed', 'Fri'],
          ),
          CustomButton(
            text: '✎ Edit ',
            header: true,
            fontSize: 18,
            colorType: 2,
            borderRadius: 32,
            width: 150,
          ),
        ],
      ),
    );
  }
}
