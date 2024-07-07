import 'package:flutter/material.dart';
import 'package:wanderer/models/expense.dart';

class ExpenseComponent extends StatelessWidget {
  final Expense expense;

  const ExpenseComponent({
    Key? key,
    required this.expense,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: Container(
        color: Colors.grey[300],
        child: ListTile(
          leading: Icon(
              Icons.abc_sharp), // Dodaj ikonę jako wiodący element listTile
          title: Text(expense.title ?? ''),
          subtitle: Text('Cost: ${expense.cost!.toStringAsFixed(2)}'),
          trailing: Text(
              'Category: ${expense.category.toString()}'), // Użyj metody categoryToString do wyświetlenia kategorii
        ),
      ),
    );
  }
}
