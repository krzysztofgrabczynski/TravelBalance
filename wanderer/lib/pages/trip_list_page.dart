import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:wanderer/components/trip_component.dart';
import 'package:wanderer/pages/expense_list_page.dart';
import 'package:wanderer/providers/user_provider.dart';

class TripListPage extends StatefulWidget {
  const TripListPage({super.key});

  @override
  _TripListPageState createState() => _TripListPageState();
}

class _TripListPageState extends State<TripListPage> {
  @override
  void initState() {
    super.initState();
    Provider.of<UserProvider>(context, listen: false).fetchWholeUserData();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Trip List Page"),
        backgroundColor: Colors.green[100],
      ),
      backgroundColor: Colors.grey[100],
      body: Consumer<UserProvider>(
        builder: (context, userProvider, child) {
          if (userProvider.user == null) {
            return const Center(
              child: CircularProgressIndicator(color: Colors.green),
            );
          } else {
            return Column(
              children: [
                Expanded(
                  child: ListView.builder(
                    itemCount: userProvider.user!.trips!.length,
                    itemBuilder: (context, index) {
                      final currentTrip = userProvider.user!.trips![index];
                      return GestureDetector(
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) =>
                                  ExpenseListPage(trip: currentTrip),
                            ),
                          );
                        },
                        child: TripComponent(trip: currentTrip),
                      );
                    },
                  ),
                ),
                ElevatedButton(
                  onPressed: () {
                    userProvider.addTrip();
                  },
                  child: const Text("Add Trip"),
                ),
              ],
            );
          }
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Provider.of<UserProvider>(context, listen: false)
              .fetchWholeUserData();
        },
        backgroundColor: Colors.green,
        child: const Icon(Icons.refresh),
      ),
    );
  }
}
