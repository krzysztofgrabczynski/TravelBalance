import 'package:flutter/material.dart';
import 'package:wanderer/pages/trip_list_page.dart';
import 'package:wanderer/services/api_service.dart';

class LoginPage extends StatelessWidget {
  const LoginPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    TextEditingController usernameController = TextEditingController();
    TextEditingController passwordController = TextEditingController();

    return Scaffold(
      appBar: AppBar(
        title: Text("Login Page"),
        backgroundColor: Colors.green[100],
      ),
      backgroundColor: Colors.grey[100],
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: usernameController,
              decoration: InputDecoration(
                labelText: 'Username',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 16),
            TextField(
              controller: passwordController,
              obscureText: true,
              decoration: InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: () async {
                // Tu umieść logikę do logowania
                String username = usernameController.text;
                String password = passwordController.text;
                // Przykładowa logika logowania
                bool result = await ApiService().login(username, password);
                if (result) {
                  // Tutaj przenieś użytkownika do kolejnej strony
                  Navigator.pushReplacement(
                    context,
                    MaterialPageRoute(
                      builder: (context) => TripListPage(),
                    ),
                  );
                } else {
                  // Tutaj wyświetl komunikat błędu logowania
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text('Invalid username or password'),
                      duration: Duration(seconds: 3),
                    ),
                  );
                }
              },
              child: Text('Login'),
            ),
          ],
        ),
      ),
    );
  }
}
