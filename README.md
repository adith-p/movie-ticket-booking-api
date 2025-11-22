### My thought process
I chose to split the project into two separate apps

one for users and one for the core business logic. This lets me isolate the moving parts, keep user-specific features inside the user app, and avoid cluttered serializers. I followed the ***fat serializers, skinny views*** pattern in DRF, where the booking logic and race-condition handling are all managed inside the serializers.

According to the requirements, we have two tables: Show and Booking.
-    The Show model includes a ```total_seats field```, which plays a key role in preventing overbooking.
-   The Booking model contains two important fields: ```seat_number``` and ```status```

All three of these fields work together to prevent overbooking and double booking.

When a new booking is created, the system validates the requested seat against the show’s ```total_seats``` and checks existing bookings (via ```seat_number``` and ```status```) to ensure the seat is still available.

The system first checks whether there’s an active show scheduled for the selected movie.
-  If the show exists, the system requests a lock on that specific row.
-  Once the lock is acquired, it validates whether the requested ```seat_number``` falls within the allowed range.
-  After validation, the system retrieves the ```curr_bookings``` from the Booking table to ensure we’re not overbooking. This is verified by checking that ```curr_bookings.count()``` does not exceed the show’s ```total_seats```.
-  The system uses the ```status``` field as one of the filter parameters when retrieving ```curr_bookings```, so only active bookings are returned. This also makes cancellation easier, as freeing a seat simply requires updating the booking’s status.
-  After that, the system checks whether the requested seat overlaps with any existing active booking. If there’s no conflict, the seat is booked; otherwise, a 409 Conflict is raised.

While all of this is happening, any other request attempting to book or modify the same show is placed in a queue until the lock is released.

