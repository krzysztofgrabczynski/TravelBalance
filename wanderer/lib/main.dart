import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:wanderer/pages/login_page.dart';
import 'package:wanderer/pages/trip_list_page.dart';
import 'package:wanderer/providers/user_provider.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => UserProvider()),
      ],
      child: MaterialApp(
        debugShowCheckedModeBanner: false,
        home: LoginPage(),
      ),
    );
  }
}
