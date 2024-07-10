import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:wanderer/components/globals.dart';
import 'package:wanderer/components/trip_component.dart';
import 'package:wanderer/models/trip.dart';
import 'package:wanderer/pages/expense_list_page.dart';
import 'package:wanderer/providers/user_provider.dart';

class TripListPage extends StatefulWidget {
  const TripListPage({super.key});

  @override
  _TripListPageState createState() => _TripListPageState();
}

class _TripListPageState extends State<TripListPage> {
  void moveToDetails(Trip currentTrip) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ExpenseListPage(trip: currentTrip),
      ),
    );
  }

  @override
  void initState() {
    super.initState();
    Provider.of<UserProvider>(context, listen: false).fetchWholeUserData();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "List of trips",
          style: TextStyle(color: Colors.white),
        ),
        backgroundColor: leadingColor,
        iconTheme: const IconThemeData(color: Colors.white),
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
                      return TripComponent(
                        trip: currentTrip,
                        moveToDetails: () => moveToDetails(currentTrip),
                      );
                    },
                  ),
                ),
                // ElevatedButton(
                //   onPressed: () {
                //     userProvider.addTrip();
                //   },
                //   child: const Text("Add Trip"),
                // ),
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
        child: const Icon(
          Icons.add,
          color: Colors.white,
        ),
      ),
    );
  }
}
