import 'package:flutter/material.dart';
import 'package:wanderer/models/expense.dart';

class Trip {
  int? _id;
  String? _name;
  String? _image;
  double? _tripCost;
  List<Expense>? _expenses;

  Trip(
      {required int id,
      required String name,
      required String? image,
      required double tripCost,
      required List<Expense> expenses})
      : _id = id,
        _name = name,
        _image = image,
        _tripCost = tripCost,
        _expenses = expenses;

  int? get id => _id;
  String? get name => _name;
  String? get image => _image;
  double? get tripCost => _tripCost;
  List<Expense>? get expenses => _expenses;

  factory Trip.fromJson(Map<String, dynamic> data) {
    final int id = data['id'];
    final String name = data['name'];
    final String? image = data['image'];
    final double tripCost = data['trip_cost'].toDouble();
    final List<Expense> expenses = (data['expenses'] as List)
        .map((expenseData) => Expense.fromJson(expenseData))
        .toList();
    return Trip(
        id: id,
        name: name,
        image: image,
        tripCost: tripCost,
        expenses: expenses);
  }

  void printDetails() {
    debugPrint('  Trip Details:');
    debugPrint('  ID: $_id');
    debugPrint('  Name: $_name');
    debugPrint(_image != null ? '  Image: $_image' : '  Image: Not Specified');
    debugPrint('  Trip Cost: $_tripCost');
    debugPrint('  Expenses:');
    for (var expense in _expenses!) {
      expense.printDetails();
    }
  }

  //No setters - no editable.
}
