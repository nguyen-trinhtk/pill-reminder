import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:frontend/const.dart';
import 'package:frontend/tabs/home.dart';
import 'package:frontend/tabs/meds.dart';
import 'package:frontend/secondary_views.dart/new_prescription.dart';
import 'package:frontend/tabs/dispenser.dart';
import 'package:frontend/tabs/account.dart';

Future<void> main() async {
  // WidgetsFlutterBinding.ensureInitialized();
  runApp(const NavigationBarApp());
}

class NavigationBarApp extends StatelessWidget {
  const NavigationBarApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme(
          brightness: Brightness.light,
          primary: kAccentColor1,
          onPrimary: kTextColor,
          secondary: kAccentColor2,
          onSecondary: kTextColor,
          surface: kBackgroundColor,
          onSurface: kTextColor,
          error: kError,
          onError: Colors.white,
          tertiary: kAccentColor3,
          onTertiary: Colors.white,
        ),
        scaffoldBackgroundColor: kBackgroundColor,
        textTheme: GoogleFonts.interTextTheme(
          ThemeData.light().textTheme,
        ).copyWith(
          headlineLarge: GoogleFonts.righteous(fontWeight: FontWeight.bold),
          headlineMedium: GoogleFonts.righteous(fontWeight: FontWeight.bold),
          headlineSmall: GoogleFonts.righteous(fontWeight: FontWeight.bold),
        ),
        navigationBarTheme: NavigationBarThemeData(
          labelTextStyle: WidgetStateProperty.all(
            TextStyle(color: kBackgroundColor),
          ),
        iconTheme: WidgetStateProperty.all(
            IconThemeData(color: kBackgroundColor),
          ),
        ),
      ),
      home: const MyApp(),
    );
  }
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  int currentPageIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      bottomNavigationBar: NavigationBar(
        onDestinationSelected: (int index) {
          setState(() {
            currentPageIndex = index;
          });
        },
        indicatorColor: kAccentColor3,
        backgroundColor: kTextColor,
        selectedIndex: currentPageIndex,
        destinations: const <Widget>[
          NavigationDestination(
            selectedIcon: Icon(Icons.home),
            icon: Icon(Icons.home_outlined),
            label: 'Home',
          ),
          NavigationDestination(
            selectedIcon: Icon(Icons.medical_services),
            icon: Icon(Icons.medical_services_outlined),
            label: 'Medication',
          ),
          NavigationDestination(
            selectedIcon: Icon(Icons.add_box_rounded),
            icon: Icon(Icons.add_box_outlined),
            label: 'Add',
          ),
          NavigationDestination(
            selectedIcon: Icon(Icons.local_pharmacy),
            icon: Icon(Icons.local_pharmacy_outlined),
            label: 'Dispenser',
          ),
          NavigationDestination(
            selectedIcon: Icon(Icons.account_circle),
            icon: Icon(Icons.account_circle_outlined),
            label: 'Account',
          ),
        ],
      ),
      body:
          <Widget>[
            HomePage(),
            MedsPage(),
            AddPage(),
            DispenserPage(),
            AccountPage(),
          ][currentPageIndex],
    );
  }
}
