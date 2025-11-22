## Requirements
* **JWT Authentication:** Secure Signup and Login endpoints.
* **Movie & Show Management:** Browse movies and available showtimes.
* **Booking System:** Book seats with strict validation (seat range, availability).
* **Concurrency Handling:** Uses database locking (`select_for_update`) to prevent race conditions.
* **Security:** Users can only view and cancel their own bookings.
* **API Documentation:** Integrated Swagger UI (`drf-spectacular`).

## Tech Stack
* **Python 3.13+**
* **Django 5.2** & **Django REST Framework**
* **SQLite** (Default DB)
* **drf-spectacular** (OpenAPI 3.0 Documentation)
* **uv** (Dependency Management)

## Setup Instructions
**Clone the repository and cd:**
    ```
    git clone (https://github.com/adith-p/movie-ticket-booking-api)
    ```
  ```
     cd movie-ticket-booking-api
   ```

1.  **Install Dependencies:**
   ```
pip install -r requirements.txt
```
or
```
uv sync
```

2.  **Apply Migrations:**
   ```
python manage.py migrate
```
or
```
uv run manage.py migrate
```
