
import 'package:flutter/material.dart';
import 'package:wanderer/components/custom_text_field.dart';
import 'package:wanderer/components/login_button_component.dart';
import 'package:wanderer/pages/forgot_password_page.dart';
import 'package:wanderer/pages/sign_up_page.dart';
import '../components/globals.dart';

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    TextEditingController usernameController = TextEditingController();
    TextEditingController passwordController = TextEditingController();

    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;

    final horizontalPadding = screenWidth * 0.05;
    final heightTextPadding = screenHeight * 0.02;
    final heightSpacerPadding = screenHeight * 0.01;
    final heightSpacerPaddingBtw = screenHeight * 0.08;
    return Scaffold(
      backgroundColor: Colors.grey[100],
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: EdgeInsets.symmetric(horizontal: horizontalPadding),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Padding(
                  padding: EdgeInsets.fromLTRB(0, 0, 0, 20),
                  child: Icon(
                    Icons.houseboat_sharp,
                    color: leadingColor,
                    size: 40,
                  ),
                ),
                const Text(
                  "Welcome back wanderer!",
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 28),
                ),
                Padding(
                  padding: EdgeInsets.symmetric(vertical: heightTextPadding),
                  child: const Text(
                    "Create your next journey here.",
                    style: TextStyle(fontSize: 18),
                  ),
                ),
                SizedBox(
                  height: heightSpacerPaddingBtw,
                ),
                CustomTextField(
                  hintText: "Username",
                  controller: usernameController,
                  obscureText: false,
                  horizontalPadding: horizontalPadding,
                ),
                CustomTextField(
                  hintText: "Password",
                  controller: passwordController,
                  obscureText: true,
                  horizontalPadding: horizontalPadding,
                ),
                SizedBox(height: heightSpacerPadding),
                LoginButtonComponent(
                  usernameController: usernameController,
                  passwordController: passwordController,
                  horizontalPadding: horizontalPadding,
                ),
                Padding(
                  padding: EdgeInsets.symmetric(
                      horizontal: horizontalPadding,
                      vertical: heightSpacerPadding),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      GestureDetector(
                        onTap: () {
                          Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => const ForgotPasswordPage()));
                        },
                        child: const Text(
                          "Forgot password?",
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ),
                      GestureDetector(
                        onTap: () {
                          Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => const SignUpPage()));
                        },
                        child: const Text("Sign up",
                            style: TextStyle(fontWeight: FontWeight.bold)),
                      ),
                    ],
                  ),
                )
              ],
            ),
          ),
        ),
      ),
    );
  }
}
