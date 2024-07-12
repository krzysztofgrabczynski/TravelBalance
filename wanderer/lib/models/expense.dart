import 'package:flutter/material.dart';

enum Category { accommodation, food, health, transport, activities, others }

class Expense {
  int _id;
  String _title;
  double _cost;
  Category _category;
  DateTime _dateTime;

  Expense({
    required int id,
    required String title,
    required double cost,
    required Category category,
    required DateTime dateTime,
  })  : _id = id,
        _title = title,
        _cost = cost,
        _category = category,
        _dateTime = dateTime;

  int get id => _id;
  String get title => _title;
  double get cost => _cost;
  Category get category => _category;
  DateTime get dateTime => _dateTime;

  factory Expense.fromJson(Map<String, dynamic> data) {
    final int id = data['id'];
    final String title = data['title'];
    final double cost = data['cost'].toDouble();
    final Category category = Category.values[data['category']];
    //Might cause problems.
    DateTime? dateTime = data['data'];
    dateTime = dateTime ?? DateTime(0);
    return Expense(
        id: id,
        title: title,
        cost: cost,
        category: category,
        dateTime: dateTime);
  }

  void printDetails() {
    debugPrint('      Expense Details:');
    debugPrint('      ID: $_id');
    debugPrint('      Title: $_title');
    debugPrint('      Cost: $_cost');
    debugPrint('      Category: $_category');
    debugPrint('      DateTime: $_dateTime');
    debugPrint('      --------------------------');
  }

  //No setters - no editable.
}
