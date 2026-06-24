# Aircraft Tickets Backend API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
Most endpoints require JWT authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Authentication Endpoints

### Register User
**POST** `/api/auth/register/`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "password2": "securepassword",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "date_joined": "2024-01-01T00:00:00Z"
  },
  "tokens": {
    "refresh": "refresh_token_here",
    "access": "access_token_here"
  },
  "message": "User registered successfully"
}
```

### Login
**POST** `/api/auth/login/`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "refresh": "refresh_token_here",
    "access": "access_token_here"
  },
  "message": "Login successful"
}
```

### Logout
**POST** `/api/auth/logout/`
**Auth Required:** Yes

**Request Body:**
```json
{
  "refresh_token": "refresh_token_here"
}
```

### Refresh Token
**POST** `/api/auth/token/refresh/`

**Request Body:**
```json
{
  "refresh": "refresh_token_here"
}
```

### Get User Profile
**GET** `/api/auth/profile/`
**Auth Required:** Yes

### Update User Profile
**PUT/PATCH** `/api/auth/profile/`
**Auth Required:** Yes

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

### Change Password
**POST** `/api/auth/change-password/`
**Auth Required:** Yes

**Request Body:**
```json
{
  "old_password": "oldpassword",
  "new_password": "newpassword",
  "new_password2": "newpassword"
}
```

---

## Flight Endpoints

### Get All Cities
**GET** `/api/flights/cities/`

**Response:**
```json
[
  {
    "id": 1,
    "code": "THR",
    "name": "Tehran",
    "country": "Iran"
  }
]
```

### Search Flights
**POST** `/api/flights/search/`

**Request Body:**
```json
{
  "origin": "THR",
  "destination": "MHD",
  "departure_date": "2024-12-25",
  "return_date": "2024-12-30",
  "passengers": 2,
  "flight_class": "economy"
}
```

**Response:**
```json
{
  "flights": [
    {
      "id": 1,
      "airline": "Iran Air",
      "logo": "https://example.com/logo.png",
      "flight_number": "IR123",
      "origin": "THR",
      "destination": "MHD",
      "departure_time": "2024-12-25T10:00:00Z",
      "arrival_time": "2024-12-25T11:30:00Z",
      "duration": "1h 30m",
      "price": "1500000.00",
      "available_seats": 50,
      "stops": 0,
      "flight_class": "economy",
      "features": ["Meal", "WiFi"]
    }
  ],
  "count": 1
}
```

### Get Flight Details
**GET** `/api/flights/<id>/`

### Get Popular Flights
**GET** `/api/flights/popular/`

**Response:**
```json
[
  {
    "id": 1,
    "from_city": "Tehran",
    "to_city": "Mashhad",
    "from_code": "THR",
    "to_code": "MHD",
    "price": "از ۱,۵۰۰,۰۰۰ تومان",
    "image": "https://example.com/image.jpg",
    "is_active": true,
    "order": 1
  }
]
```

### Get Popular Destinations
**GET** `/api/flights/destinations/`

**Response:**
```json
[
  {
    "id": 1,
    "title": "Dubai",
    "subtitle": "United Arab Emirates",
    "image": "https://example.com/dubai.jpg",
    "destination_code": "DXB",
    "is_active": true,
    "order": 1
  }
]
```

### List/Create Flights (Admin)
**GET/POST** `/api/flights/`
**Auth Required:** Admin only for POST

### Update/Delete Flight (Admin)
**PUT/PATCH/DELETE** `/api/flights/<id>/manage/`
**Auth Required:** Admin only

---

## Transport Endpoints (Bus & Train)

### Search Transport
**POST** `/api/transport/search/`

**Request Body:**
```json
{
  "transport_type": "bus",
  "origin": "Tehran",
  "destination": "Isfahan",
  "departure_date": "2024-12-25",
  "passengers": 2
}
```

**Response:**
```json
{
  "trips": [
    {
      "id": 1,
      "transport_type": "bus",
      "company": "Iran Peyma",
      "logo": "https://example.com/logo.png",
      "trip_number": "IP123",
      "origin": "Tehran",
      "destination": "Isfahan",
      "departure_time": "2024-12-25T08:00:00Z",
      "arrival_time": "2024-12-25T14:00:00Z",
      "duration": "6h",
      "price": "500000.00",
      "available_seats": 30,
      "features": ["AC", "WiFi", "Toilet"]
    }
  ],
  "count": 1
}
```

### Get Transport Trip Details
**GET** `/api/transport/<id>/`

### List/Create Transport Trips (Admin)
**GET/POST** `/api/transport/`
**Auth Required:** Admin only for POST

### Update/Delete Transport Trip (Admin)
**PUT/PATCH/DELETE** `/api/transport/<id>/manage/`
**Auth Required:** Admin only

---

## Insurance Endpoints

### Get Insurance Plans
**GET** `/api/insurance/plans/`

**Response:**
```json
[
  {
    "id": 1,
    "title": "Basic Travel Insurance",
    "price": "200000.00",
    "coverage": "Up to $50,000",
    "popular": false,
    "features": ["Medical Coverage", "Trip Cancellation"],
    "is_active": true
  }
]
```

### Get Insurance Plan Details
**GET** `/api/insurance/plans/<id>/`

### Create Insurance Booking
**POST** `/api/insurance/bookings/`

**Request Body:**
```json
{
  "plan": 1,
  "first_name": "John",
  "last_name": "Doe",
  "national_id": "1234567890",
  "birth_date": "1990-01-01",
  "destination": "Dubai",
  "start_date": "2024-12-25",
  "end_date": "2024-12-30",
  "phone": "+1234567890",
  "email": "john@example.com"
}
```

**Response:**
```json
{
  "id": 1,
  "plan": 1,
  "plan_details": {...},
  "tracking_code": "ABC1234567",
  "status": "pending",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Get My Insurance Bookings
**GET** `/api/insurance/my-bookings/`
**Auth Required:** Yes

### Get Insurance Booking by Tracking Code
**GET** `/api/insurance/bookings/<tracking_code>/`

---

## Booking Endpoints

### Create Booking
**POST** `/api/bookings/create/`

**Request Body (Flight):**
```json
{
  "booking_type": "flight",
  "flight": 1,
  "passengers": [
    {
      "first_name": "John",
      "last_name": "Doe",
      "national_id": "1234567890",
      "birth_date": "1990-01-01",
      "gender": "male"
    }
  ],
  "contact_email": "john@example.com",
  "contact_phone": "+1234567890",
  "total_price": "1500000.00",
  "seat_numbers": ["12A", "12B"]
}
```

**Request Body (Bus/Train):**
```json
{
  "booking_type": "bus",
  "transport_trip": 1,
  "passengers": [
    {
      "first_name": "John",
      "last_name": "Doe",
      "national_id": "1234567890",
      "birth_date": "1990-01-01",
      "gender": "male"
    }
  ],
  "contact_email": "john@example.com",
  "contact_phone": "+1234567890",
  "total_price": "500000.00",
  "seat_numbers": ["15"]
}
```

**Response:**
```json
{
  "booking": {
    "id": 1,
    "tracking_code": "XYZ9876543",
    "booking_type": "flight",
    "status": "pending",
    "total_price": "1500000.00",
    "flight_details": {...},
    "passengers": [...],
    "created_at": "2024-01-01T00:00:00Z"
  },
  "message": "Booking created successfully"
}
```

### Get My Bookings
**GET** `/api/bookings/my-bookings/`
**Auth Required:** Yes

### Get My Tickets (All)
**GET** `/api/bookings/my-tickets/`
**Auth Required:** Yes

### Get Booking by Tracking Code
**GET** `/api/bookings/<tracking_code>/`

### Cancel Booking
**POST** `/api/bookings/<tracking_code>/cancel/`
**Auth Required:** Yes

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid data",
  "details": {
    "field_name": ["Error message"]
  }
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Notes

1. All datetime fields are in ISO 8601 format (UTC)
2. Prices are in Iranian Rials (decimal format)
3. Tracking codes are unique 10-character alphanumeric strings
4. JWT tokens expire after 60 minutes (access) and 24 hours (refresh)
5. Pagination is available on list endpoints (default: 20 items per page)

---

## Testing the API

You can test the API using tools like:
- Postman
- cURL
- HTTPie
- Python requests library

Example cURL request:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'