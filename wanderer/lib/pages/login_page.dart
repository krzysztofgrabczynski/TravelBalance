import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:wanderer/components/custom_text_field.dart';
import 'package:wanderer/pages/trip_list_page.dart';
import 'package:wanderer/providers/auth_provider.dart';
import '../components/globals.dart';

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    TextEditingController usernameController = TextEditingController();
    TextEditingController passwordController = TextEditingController();

    return Scaffold(
      backgroundColor: Colors.grey[100],
      body: SafeArea(
        child: Center(
          child: Column(
            children: [
              Padding(
                padding: const EdgeInsets.all(100.0),
                child: Icon(
                  Icons.houseboat_sharp,
                  color: leadingColor,
                  size: 40,
                ),
              ),
              Text(
                "Welcome back wanderer!",
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 28),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 8),
                child: Text(
                  "Create your next journey here.",
                  style: TextStyle(fontSize: 18),
                ),
              ),
              SizedBox(
                height: 50,
              ),
              CustomTextField(
                hintText: "Username",
                controller: usernameController,
                obscureText: false,
              ),
              CustomTextField(
                hintText: "Password",
                controller: passwordController,
                obscureText: true,
              ),
              SizedBox(height: 4),
              Consumer<AuthProvider>(
                builder: (context, authProvider, child) {
                  return ElevatedButton(
                    onPressed: authProvider.isLoading
                        ? null
                        : () async {
                            bool success = await authProvider.login(
                              usernameController.text,
                              passwordController.text,
                            );
                            if (success) {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (context) => TripListPage()),
                              );
                            }
                          },
                    child: authProvider.isLoading
                        ? SizedBox(
                            width: 24,
                            height: 24,
                            child: CircularProgressIndicator(
                              color: Colors.white, // Kolor kółka ładowania
                              strokeWidth: 2.0,
                            ),
                          )
                        : Text("Login"),
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
