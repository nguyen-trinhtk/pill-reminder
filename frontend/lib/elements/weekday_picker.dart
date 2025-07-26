import 'package:flutter/material.dart';
import 'package:frontend/const.dart';
import 'package:google_fonts/google_fonts.dart';

final List<String> weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

class WeekdayPicker extends StatefulWidget {
  final Function(List<int>)? onSelected;
  final bool selectable;
  final List<String> initialSelected;

  const WeekdayPicker({
    Key? key,
    this.onSelected,
    this.selectable = false,
    this.initialSelected = const [],
  }) : super(key: key);

  @override
  State<WeekdayPicker> createState() => _WeekdayPickerState();
}

class _WeekdayPickerState extends State<WeekdayPicker> {
  @override
  void didUpdateWidget(covariant WeekdayPicker oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.initialSelected != oldWidget.initialSelected) {
      selectedIndices =
          widget.initialSelected
              .map(
                (day) => weekdays.indexWhere((w) => w == day || w[0] == day[0]),
              )
              .where((i) => i != -1)
              .toList();
    }
  }

  late List<int> selectedIndices;

  @override
  void initState() {
    super.initState();
    selectedIndices =
        widget.initialSelected
            .map(
              (day) => weekdays.indexWhere((w) => w == day || w[0] == day[0]),
            )
            .where((i) => i != -1)
            .toList();
  }

  @override
  Widget build(BuildContext context) {
    final List<int> displaySelectedIndices =
        widget.selectable
            ? selectedIndices
            : widget.initialSelected
                .map(
                  (day) =>
                      weekdays.indexWhere((w) => w == day || w[0] == day[0]),
                )
                .where((i) => i != -1)
                .toList();
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: List.generate(weekdays.length, (index) {
        final bool isSelected = displaySelectedIndices.contains(index);
        return Expanded(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 2.0),
            child: GestureDetector(
              onTap:
                  widget.selectable
                      ? () {
                        setState(() {
                          if (isSelected) {
                            selectedIndices.remove(index);
                          } else {
                            selectedIndices.add(index);
                          }
                          if (widget.onSelected != null) {
                            widget.onSelected!(selectedIndices);
                          } else {
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                content: Text(
                                  'Selected days: $selectedIndices',
                                ),
                              ),
                            );
                          }
                        });
                      }
                      : null,
              child: Container(
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(color: kTextColor, width: 2.0),
                  color: isSelected ? kAccentColor3 : kAccentColor2,
                ),
                alignment: Alignment.center,
                child: Text(
                  weekdays[index][0],
                  style: GoogleFonts.righteous(
                    color: isSelected ? Colors.white : kTextColor,
                    fontWeight: FontWeight.bold,
                    fontSize: 20,
                  ),
                ),
              ),
            ),
          ),
        );
      }),
    );
  }
}
