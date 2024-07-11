import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:wanderer/models/expense.dart';

class ExpenseComponent extends StatelessWidget {
  final Expense expense;

  const ExpenseComponent({
    super.key,
    required this.expense,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(8.0.w),
      child: Container(
        color: Colors.grey[300],
        child: ListTile(
          leading: const Icon(
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
