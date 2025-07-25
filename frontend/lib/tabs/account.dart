import 'package:flutter/material.dart';
import 'package:frontend/elements/appbar.dart';
import 'package:frontend/elements/text.dart';

class AccountPage extends StatelessWidget {
  const AccountPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        title: 'Account',
      ),
      body: Center(
        child: CustomText(text:'Account Page')
      ),
    );
  }
}

