import 'package:flutter/foundation.dart';
import 'package:wanderer/models/user.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static final ApiService _instance = ApiService._internal();

  ApiService._internal();
  static const String _baseToken = "Token ";
  static String? _token = "dcb18eaa602e7296c9921ab5b618d64047e148b6";
  static const String _baseUrl =
      "http://wanderer-test-fe529f1fdf47.herokuapp.com/api/v1/";

  factory ApiService() {
    return _instance;
  }

  void setUserToken(String token) {
    _token = token;
  }

  Future<User?> fetchWholeUserData() async {
    try {
      var endpoint = 'trip/get_trip_with_expenses/';
      var response = await http.get(Uri.parse('$_baseUrl$endpoint'),
          headers: {'Authorization': '$_baseToken$_token'});

      if (response.statusCode == 200) {
        return User.fromJson(jsonDecode(response.body));
      } else {
        debugPrint('Request failed with status: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      debugPrint("Error in fetchWholeUserData: $e");
      return null;
    }
  }
}
