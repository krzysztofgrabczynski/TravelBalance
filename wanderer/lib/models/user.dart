import 'package:flutter/material.dart';
import 'package:wanderer/models/trip.dart';

class User {
  List<Trip>? _trips;

  User({required List<Trip> trips}) : _trips = trips;

  List<Trip>? get trips => _trips;

  factory User.fromJson(List<dynamic> jsonList) {
    List<Trip> trips = jsonList.map((jsonData) => Trip.fromJson(jsonData)).toList();
    return User(trips: trips);
  }

  printDetails() {
    debugPrint('User Trips:');
    for (var trip in _trips!) {
      trip.printDetails();
    }
  }
}
