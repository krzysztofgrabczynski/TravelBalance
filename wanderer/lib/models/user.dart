import 'package:wanderer/models/trip.dart';

class User {
  List<Trip>? _trips;

  User({required List<Trip> trips}) : _trips = trips;

  List<Trip>? get trips => _trips;

  printDetails() {
    for (var trip in _trips!) {
      trip.printDetails();
    }
  }
}
