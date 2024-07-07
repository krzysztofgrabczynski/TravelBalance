import 'package:flutter/foundation.dart';
import 'package:wanderer/models/trip.dart';
import 'package:wanderer/models/user.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static final ApiService _instance = ApiService._internal();

  ApiService._internal();

  String? _token = "dcb18eaa602e7296c9921ab5b618d64047e148b6";
  static const String baseUrl =
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
      var response = await http.get(Uri.parse('$baseUrl$endpoint'),
          headers: {'Authorization': _token!});

      if (response.statusCode == 200) {
        var jsonData = jsonDecode(response.body);
        return User.fromJson(jsonData);
      }
    } catch (e) {
      print("Error in fetchWholeUserData: $e");
      rethrow;
    }
  }
}
