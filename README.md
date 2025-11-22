**Objective:** Design and implement a backend system for a Movie Ticket Booking application using Django and Django REST Framework.

* By Adith-p
###  Tech Stack
* **Language:** Python
* **Frameworks:** Django, Django REST Framework
* **Authentication:** JWT (JSON Web Tokens)
* **Documentation:** Swagger (drf-spectacular/drf-yasg)

###  Database Models
1.  **Movie:** `title`, `duration_minutes`
2.  **Show:** `movie` (FK), `screen_name`, `date_time`, `total_seats`
3.  **Booking:** `user` (FK), `show` (FK), `seat_number`, `status` (booked/cancelled), `created_at`

###  API Endpoints
* **Auth:**
    * `POST /signup` (Register user)
    * `POST /login` (Get JWT token)
* **Movies & Shows:**
    * `GET /movies/` (List all movies)
    * `GET /movies/<id>/shows/` (List shows for a movie)
* **Booking:**
    * `POST /shows/<id>/book/` (Book a seat)
    * `POST /bookings/<id>/cancel/` (Cancel booking)
    * `GET /my-bookings/` (List user's bookings)

###  Business Rules
1.  **Double Booking:** A seat cannot be booked twice for the same show.
2.  **Overbooking:** Bookings cannot exceed the total seats defined for a show.
3.  **Cancellation:** Cancelling a booking must make the seat available again immediately.

### Documentation & Deliverables
* API documentation must be available at `/swagger/`.
* All booking endpoints must require a valid JWT.
* The project must handle concurrency (prevent race conditions).

### Installation 

```
  git clone https://github.com/adith-p/movie-ticket-booking-api
  cd movie-ticket-booking-api
```
Install Dependencies:

using pip
```
pip Install -r requirements.txt
```
using uv
```
uv sync
```
```
source .venv/bin/activate
```
Apply Migrations:

using pip
```
python manage.py migrate
```
using uv
```
uv run manage migrate
```
Runserver

using pip
```
python manage.py runserver
```
using uv
```
uv run manage.py runserver
```

### My thought process
I chose to split the project into two separate apps

one for users and one for the core business logic. This lets me isolate the moving parts, keep user-specific features inside the user app, and avoid cluttered serializers. I followed the ***fat serializers, skinny views*** pattern in DRF, where the booking logic and race-condition handling are all managed inside the serializers.

According to the requirements, we have two tables: Show and Booking.
*    The Show model includes a ```total_seats field```, which plays a key role in preventing overbooking.
*   The Booking model contains two important fields: ```seat_number``` and ```status```

All three of these fields work together to prevent overbooking and double booking.

When a new booking is created, the system validates the requested seat against the show’s ```total_seats``` and checks existing bookings (via ```seat_number``` and ```status```) to ensure the seat is still available.

The system first checks whether there’s an active show scheduled for the selected movie.
*  If the show exists, the system requests a lock on that specific row.
*  Once the lock is acquired, it validates whether the requested ```seat_number``` falls within the allowed range.
*  After validation, the system retrieves the ```curr_bookings``` from the Booking table to ensure we’re not overbooking. This is verified by checking that ```curr_bookings.count()``` does not exceed the show’s ```total_seats```.
*  The system uses the ```status``` field as one of the filter parameters when retrieving ```curr_bookings```, so only active bookings are returned. This also makes cancellation easier, as freeing a seat simply requires updating the booking’s status.
*  After that, the system checks whether the requested seat overlaps with any existing active booking. If there’s no conflict, the seat is booked; otherwise, a 409 Conflict is raised.

While all of this is happening, any other request attempting to book or modify the same show is placed in a queue until the lock is released.
To ensure data integrity, the system wraps the entire booking process inside a ```transaction.atomic()``` block.
