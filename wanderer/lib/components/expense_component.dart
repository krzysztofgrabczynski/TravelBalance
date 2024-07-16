import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:wanderer/models/expense.dart';

class ExpenseComponent extends StatelessWidget {
  final Expense expense;

  Widget categoryIcon(Category category) {
    Map<Category, MapEntry<IconData, Color>> categoryIcon = {
      Category.accommodation: const MapEntry(Icons.hotel, Color(0xFFfedab3)),
      Category.food: const MapEntry(Icons.restaurant, Color(0xFFc4f3c8)),
      Category.health: const MapEntry(Icons.local_hospital, Color(0xFFfbc1b9)),
      Category.transport:
          const MapEntry(Icons.directions_car, Color(0xFFaad3fe)),
      Category.activities:
          const MapEntry(Icons.local_activity, Color(0xFFc8c7f1)),
      Category.others: const MapEntry(Icons.category, Color(0xFFffeea4)),
    };

    IconData icon = categoryIcon[category]?.key ?? Icons.error;
    Color color = categoryIcon[category]?.value ?? Colors.grey;

    return Stack(
      alignment: Alignment.center,
      children: [
        Container(
          width: 45.w,
          height: 45.h,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(1000),
            color: color,
          ),
        ),
        Icon(
          icon,
          size: 23.h,
        ),
      ],
    );
  }

  const ExpenseComponent({
    super.key,
    required this.expense,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(4.0.w),
      child: ListTile(
        leading: categoryIcon(expense.category),
        title: Text(expense.title),
        trailing: Text(
          '\$${expense.cost.toStringAsFixed(2)}',
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16.sp),
        ),
        subtitle: Text(expense.categoryToString()),
      ),
    );
  }
}
