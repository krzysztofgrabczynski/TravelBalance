import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:wanderer/components/expense_component.dart';
import 'package:wanderer/models/trip.dart';

class ExpenseListPage extends StatelessWidget {
  final Trip trip;

  ExpenseListPage({
    Key? key,
    required this.trip,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(trip.name!),
        backgroundColor: Colors.green[100],
      ),
      backgroundColor: Colors.grey[100],
      body: ListView.builder(
        itemCount: trip.expenses!.length,
        itemBuilder: (context, index) {
          final expense = trip.expenses![index];
          return ExpenseComponent(expense: expense);
        },
      ),
    );
  }
}
