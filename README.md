# Aircraft Tickets Backend

Django REST API backend with MongoDB for the Aircraft Tickets booking system.

## Features

- JWT Authentication
- Flight booking system
- Bus and Train booking
- Travel insurance
- User management
- MongoDB database
- RESTful API

## Tech Stack

- Django 4.2.7
- Django REST Framework
- MongoDB (via Djongo)
- JWT Authentication
- CORS support

## Prerequisites

- Python 3.8+
- MongoDB Atlas account (or local MongoDB)
- pip (Python package manager)

## Installation

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
```

3. **Activate virtual environment:**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Create .env file:**
```bash
copy .env.example .env
```

6. **Edit .env file and add your MongoDB credentials:**
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

MONGODB_URI=mongodb+srv://rfzali93:<db_password>@cluster0.bnltfut.mongodb.net/
MONGODB_NAME=aircraft_tickets
MONGODB_PASSWORD=your-actual-password-here

JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

7. **Run migrations:**
```bash
python manage.py migrate
```

8. **Create superuser (admin):**
```bash
python manage.py createsuperuser
```

9. **Run development server:**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Documentation

See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for detailed API endpoints and usage.

## Project Structure

```
backend/
├── aircraft_tickets/       # Main project settings
│   ├── settings.py        # Django settings
│   ├── urls.py           # Main URL configuration
│   ├── wsgi.py           # WSGI configuration
│   └── asgi.py           # ASGI configuration
├── apps/                  # Django apps
│   ├── users/            # User authentication
│   ├── flights/          # Flight management
│   ├── transport/        # Bus and train management
│   ├── insurance/        # Travel insurance
│   └── bookings/         # Booking management
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables example
└── README.md            # This file
```

## Available Apps

### Users App
- User registration and authentication
- JWT token management
- User profile management
- Password change

### Flights App
- Flight search and listing
- Popular flights and destinations
- City management
- Flight booking

### Transport App
- Bus and train search
- Transport trip management
- Booking system

### Insurance App
- Insurance plans
- Insurance booking
- Coverage management

### Bookings App
- Unified booking system
- Booking tracking
- Cancellation management
- User tickets

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/`

Use the superuser credentials you created during setup.

## Testing

To run tests:
```bash
python manage.py test
```

## Common Commands

**Create new app:**
```bash
python manage.py startapp app_name
```

**Make migrations:**
```bash
python manage.py makemigrations
```

**Apply migrations:**
```bash
python manage.py migrate
```

**Create superuser:**
```bash
python manage.py createsuperuser
```

**Collect static files:**
```bash
python manage.py collectstatic
```

**Run development server:**
```bash
python manage.py runserver
```

**Run on specific port:**
```bash
python manage.py runserver 8080
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| SECRET_KEY | Django secret key | - |
| DEBUG | Debug mode | True |
| ALLOWED_HOSTS | Allowed hosts | localhost,127.0.0.1 |
| MONGODB_URI | MongoDB connection string | - |
| MONGODB_NAME | Database name | aircraft_tickets |
| MONGODB_PASSWORD | MongoDB password | - |
| JWT_ACCESS_TOKEN_LIFETIME | Access token lifetime (minutes) | 60 |
| JWT_REFRESH_TOKEN_LIFETIME | Refresh token lifetime (minutes) | 1440 |
| CORS_ALLOWED_ORIGINS | CORS allowed origins | http://localhost:3000 |

## Troubleshooting

### MongoDB Connection Issues
- Verify your MongoDB URI is correct
- Check if your IP is whitelisted in MongoDB Atlas
- Ensure the password doesn't contain special characters that need URL encoding

### Import Errors
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Migration Errors
- Delete migration files (except __init__.py) and run makemigrations again
- Check MongoDB connection

### CORS Issues
- Add your frontend URL to CORS_ALLOWED_ORIGINS in .env
- Restart the server after changing .env

## Production Deployment

1. Set DEBUG=False in .env
2. Set proper SECRET_KEY
3. Configure ALLOWED_HOSTS
4. Use production-grade WSGI server (gunicorn, uwsgi)
5. Set up proper MongoDB security
6. Use environment variables for sensitive data
7. Enable HTTPS

## License

This project is part of the Aircraft Tickets booking system.

## Support

For issues and questions, please refer to the main project documentation.