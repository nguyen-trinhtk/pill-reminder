import 'package:flutter/material.dart';
import 'package:frontend/elements/appbar.dart';
import 'package:frontend/const.dart';
import 'package:frontend/elements/text.dart';
import 'package:frontend/elements/weekday_picker.dart';
import 'package:frontend/elements/button.dart';
import 'package:flutter/services.dart';

class AddPage extends StatefulWidget {
  const AddPage({super.key});

  @override
  State<AddPage> createState() => _AddPageState();
}

class _AddPageState extends State<AddPage> {
  List<TimeOfDay> _selectedTimes = [];
  DateTime _selectedStartDate = DateTime.now();
  final List<String> _dosageUnits = [
    'pills',
    'capsules',
    'ml',
    'mg',
    'drops',
    'Custom...',
  ];
  String? _selectedDosageUnit;
  final TextEditingController _amountController = TextEditingController(
    text: '1',
  );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(title: 'New Prescription'),
      body: Padding(
        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 40),
        child: Column(
          spacing: 20,
          children: [
            CustomText(text: 'Ibuprofen', header: true, fontSize: 28),
            Row(
              spacing: 20,
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      CustomText(text: 'Amount', header: true),
                      const SizedBox(height: 8),
                      TextField(
                        controller: _amountController,
                        keyboardType: TextInputType.number,
                        decoration: InputDecoration(
                          hintText: 'e.g. 2',
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(24),
                          ),
                          contentPadding: const EdgeInsets.symmetric(
                            vertical: 8,
                            horizontal: 16,
                          ),
                          filled: true,
                          fillColor: kAccentColor2,
                        ),
                        inputFormatters: <TextInputFormatter>[
                          FilteringTextInputFormatter.digitsOnly,
                        ],
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      CustomText(text: 'Dosage', header: true),
                      const SizedBox(height: 8),
                      DropdownButtonFormField<String>(
                        value: _selectedDosageUnit,
                        items:
                            _dosageUnits
                                .map(
                                  (unit) => DropdownMenuItem(
                                    value: unit,
                                    child: Text(unit),
                                  ),
                                )
                                .toList(),
                        onChanged: (value) {
                          setState(() {
                            _selectedDosageUnit = value;
                          });
                        },
                        decoration: InputDecoration(
                          hintText: 'Select unit',
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(24),
                          ),
                          contentPadding: const EdgeInsets.symmetric(
                            vertical: 8,
                            horizontal: 16,
                          ),
                          filled: true,
                          fillColor: kAccentColor2,
                        ),
                        dropdownColor: kAccentColor2,
                      ),
                    ],
                  ),
                ),
              ],
            ),
            Row(
              spacing: 20,
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      CustomText(text: 'Time', header: true),
                      const SizedBox(height: 8),
                      GestureDetector(
                        onTap: () async {
                          List<TimeOfDay> tempTimes = List.from(_selectedTimes);
                          await showModalBottomSheet(
                            context: context,
                            shape: const RoundedRectangleBorder(
                              borderRadius: BorderRadius.vertical(
                                top: Radius.circular(24),
                              ),
                            ),
                            builder: (context) {
                              return StatefulBuilder(
                                builder: (context, modalSetState) {
                                  return Padding(
                                    padding: const EdgeInsets.all(24),
                                    child: Column(
                                      mainAxisSize: MainAxisSize.min,
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        Row(
                                          mainAxisAlignment:
                                              MainAxisAlignment.spaceBetween,
                                          children: [
                                            const Text(
                                              'Times',
                                              style: TextStyle(
                                                fontWeight: FontWeight.bold,
                                                fontSize: 18,
                                              ),
                                            ),
                                            IconButton(
                                              icon: const Icon(Icons.close),
                                              onPressed:
                                                  () => Navigator.pop(context),
                                            ),
                                          ],
                                        ),
                                        const SizedBox(height: 12),
                                        if (tempTimes.isEmpty)
                                          const Text('No times added.'),
                                        if (tempTimes.isNotEmpty)
                                          Wrap(
                                            spacing: 8,
                                            runSpacing: 8,
                                            children:
                                                tempTimes
                                                    .map(
                                                      (time) => Chip(
                                                        label: Text(
                                                          time.format(context),
                                                        ),
                                                        shape: RoundedRectangleBorder(
                                                          borderRadius:
                                                              BorderRadius.circular(
                                                                16,
                                                              ),
                                                          side: BorderSide(
                                                            color: kTextColor,
                                                            width: 1.5,
                                                          ),
                                                        ),
                                                        backgroundColor:
                                                            kAccentColor2,
                                                        deleteIcon: const Icon(
                                                          Icons.close,
                                                          size: 18,
                                                          color: kError,
                                                        ),
                                                        onDeleted: () {
                                                          modalSetState(() {
                                                            tempTimes.remove(
                                                              time,
                                                            );
                                                          });
                                                        },
                                                      ),
                                                    )
                                                    .toList(),
                                          ),
                                        const SizedBox(height: 16),
                                        Row(
                                          children: [
                                            Expanded(
                                              child: TextButton.icon(
                                                style: TextButton.styleFrom(
                                                  backgroundColor:
                                                      kAccentColor1,
                                                  foregroundColor: kTextColor,
                                                  shape: RoundedRectangleBorder(
                                                    borderRadius:
                                                        BorderRadius.circular(
                                                          24,
                                                        ),
                                                    side: const BorderSide(
                                                      width: 1,
                                                    ),
                                                  ),
                                                ),
                                                icon: const Icon(Icons.add),
                                                label: const Text('Add Time'),
                                                onPressed: () async {
                                                  TimeOfDay?
                                                  picked = await showTimePicker(
                                                    context: context,
                                                    initialTime:
                                                        TimeOfDay.now(),
                                                    builder: (context, child) {
                                                      return Theme(
                                                        data: Theme.of(
                                                          context,
                                                        ).copyWith(
                                                          textButtonTheme: TextButtonThemeData(
                                                            style: TextButton.styleFrom(
                                                              backgroundColor:
                                                                  kAccentColor3,
                                                              foregroundColor:
                                                                  kAccentColor2,
                                                              side:
                                                                  const BorderSide(
                                                                    width: 1,
                                                                  ),
                                                            ),
                                                          ),
                                                        ),
                                                        child: child!,
                                                      );
                                                    },
                                                  );
                                                  if (picked != null &&
                                                      !tempTimes.contains(
                                                        picked,
                                                      )) {
                                                    modalSetState(() {
                                                      tempTimes.add(picked);
                                                    });
                                                  }
                                                },
                                              ),
                                            ),
                                            const SizedBox(width: 12),
                                            Expanded(
                                              child: TextButton.icon(
                                                style: TextButton.styleFrom(
                                                  backgroundColor: kTextColor,
                                                  foregroundColor:
                                                      kAccentColor2,
                                                  shape: RoundedRectangleBorder(
                                                    borderRadius:
                                                        BorderRadius.circular(
                                                          24,
                                                        ),
                                                    side: const BorderSide(
                                                      width: 1,
                                                    ),
                                                  ),
                                                ),
                                                icon: const Icon(Icons.check),
                                                label: const Text('Save'),
                                                onPressed: () {
                                                  setState(() {
                                                    _selectedTimes = List.from(
                                                      tempTimes,
                                                    );
                                                  });
                                                  Navigator.pop(context);
                                                },
                                              ),
                                            ),
                                          ],
                                        ),
                                      ],
                                    ),
                                  );
                                },
                              );
                            },
                          );
                        },
                        child: Container(
                          height: 48,
                          padding: const EdgeInsets.symmetric(horizontal: 16),
                          decoration: BoxDecoration(
                            color: kAccentColor2,
                            borderRadius: BorderRadius.circular(24),
                            border: Border.all(color: kTextColor, width: 1.5),
                          ),
                          alignment: Alignment.centerLeft,
                          child: Row(
                            children: [
                              if (_selectedTimes.isEmpty)
                                Text(
                                  'Select time',
                                  style: TextStyle(color: Colors.grey[500]),
                                ),
                              if (_selectedTimes.isNotEmpty)
                                Text(
                                  _selectedTimes.first.format(context),
                                  style: TextStyle(
                                    color: kTextColor,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              Spacer(),
                              if (_selectedTimes.length > 1)
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 10,
                                    vertical: 4,
                                  ),
                                  decoration: BoxDecoration(
                                    color: kAccentColor3,
                                    borderRadius: BorderRadius.circular(16),
                                  ),
                                  child: Text(
                                    '+${_selectedTimes.length - 1}',
                                    style: const TextStyle(
                                      color: Colors.white,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      CustomText(text: 'Start Date', header: true),
                      const SizedBox(height: 8),
                      GestureDetector(
                        onTap: () async {
                          DateTime? picked = await showDatePicker(
                            context: context,
                            initialDate: _selectedStartDate,
                            firstDate: DateTime(2000),
                            lastDate: DateTime(2100),
                            builder: (context, child) {
                              return Theme(
                                data: Theme.of(context).copyWith(
                                  textButtonTheme: TextButtonThemeData(
                                    style: TextButton.styleFrom(
                                      backgroundColor: kAccentColor3,
                                      foregroundColor: kAccentColor2,
                                      side: const BorderSide(width: 1),
                                    ),
                                  ),
                                ),
                                child: child!,
                              );
                            },
                          );
                          if (picked != null) {
                            setState(() {
                              _selectedStartDate = picked;
                            });
                          }
                        },
                        child: AbsorbPointer(
                          child: TextField(
                            readOnly: true,
                            controller: TextEditingController(
                              text:
                                  "${_selectedStartDate.year}-${_selectedStartDate.month.toString().padLeft(2, '0')}-${_selectedStartDate.day.toString().padLeft(2, '0')}",
                            ),
                            decoration: InputDecoration(
                              hintText: 'Select date',
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(24),
                              ),
                              contentPadding: const EdgeInsets.symmetric(
                                vertical: 8,
                                horizontal: 16,
                              ),
                              filled: true,
                              fillColor: kAccentColor2,
                              suffixIcon: const Icon(Icons.calendar_today),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            CustomText(text: 'Frequency', header: true, fontSize: 28),
            WeekdayPicker(
              selectable: true,
              initialSelected: const ['Mon', 'Wed', 'Fri'],
            ),
            const SizedBox(height: 20),
            CustomButton(
              text: 'Add to List',
              borderRadius: 32,
              width: 240,
              header: true,
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _amountController.dispose();
    super.dispose();
  }
}
