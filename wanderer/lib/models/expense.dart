enum Category { accommodation, food, health, transport, activities, others }

class Expense {
  int? _id;
  String? _title;
  double? _cost;
  Category? _category;
  DateTime? _dateTime;

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

  int? get id => _id;
  String? get title => _title;
  double? get cost => _cost;
  Category? get category => _category;
  DateTime? get dateTime => _dateTime;

  factory Expense.fromJson(Map<String, dynamic> data) {
    //Add validations.
    final int id = data['id'];
    final String title = data['title'];
    final double cost = data['cost'];
    //Might result in problems. Contact Krzysztof abt Categories.
    final Category category = Category.values[data['category']];
    final DateTime dateTime = data['data'];
    return Expense(
        id: id,
        title: title,
        cost: cost,
        category: category,
        dateTime: dateTime);
  }

  void printDetails() {
    print('   Expense Details:');
    print('   ID: $_id');
    print('   Title: $_title');
    print('   Cost: $_cost');
    print('   Category: $_category');
    print('   DateTime: $_dateTime');
  }

  //No setters - no editable.
}
