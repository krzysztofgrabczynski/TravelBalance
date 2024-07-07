import 'package:flutter/material.dart';
import 'package:wanderer/models/trip.dart';

class TripComponent extends StatelessWidget {
  final Trip trip;

  const TripComponent({
    Key? key,
    required this.trip,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: Container(
        color: Colors.grey[300],
        child: ListTile(
          title: Text(trip.name ?? ''),
          subtitle: Text('Trip cost: ${trip.tripCost!.toStringAsFixed(2)}'),
        ),
      ),
    );
  }
}
