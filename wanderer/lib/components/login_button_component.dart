import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';
import '../pages/trip_list_page.dart';
import '../components/globals.dart';

class LoginButtonComponent extends StatelessWidget {
  final TextEditingController usernameController;
  final TextEditingController passwordController;
  final double horizontalPadding;

  const LoginButtonComponent({
    super.key,
    required this.usernameController,
    required this.passwordController,
    required this.horizontalPadding,
  });

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;

    return Consumer<AuthProvider>(
      builder: (context, authProvider, child) {
        return Padding(
          padding: EdgeInsets.symmetric(horizontal: horizontalPadding),
          child: ElevatedButton(
            onPressed: authProvider.isLoading
                ? null
                : () async {
                    bool success = await authProvider.login(
                      usernameController.text,
                      passwordController.text,
                    );
                    if (success) {
                      Navigator.pushReplacement(
                        context,
                        MaterialPageRoute(
                            builder: (context) => const TripListPage()),
                      );
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Container(
                            child: const Center(
                                child: Text('Login failed. Please try again.')),
                          ),
                          behavior: SnackBarBehavior.floating,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(24.0),
                          ),
                          margin: const EdgeInsets.all(16.0),
                        ),
                      );
                    }
                  },
            style: ButtonStyle(
              minimumSize: WidgetStateProperty.all(Size(screenWidth, 50)),
              backgroundColor: WidgetStateProperty.all(leadingColor),
            ),
            child: authProvider.isLoading
                ? const SizedBox(
                    width: 24,
                    height: 24,
                    child: CircularProgressIndicator(
                      color: Colors.white, // Kolor kółka ładowania
                      strokeWidth: 2.0,
                    ),
                  )
                : const Text(
                    "Login",
                    style: TextStyle(color: Colors.white),
                  ),
          ),
        );
      },
    );
  }
}
