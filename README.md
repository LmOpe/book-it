# Music Book API

## Overview
Music Book API is a platform that connects artists, event organizers, and users by providing a seamless way to manage artist profiles, event listings, and bookings.

## Features

### User Authentication & Authorization
- JWT-based authentication (Signup, Login, Logout).
- Role-based access control (Users, Artists, Event Organizers, Admins).

### Artist Management
- Artists can create and update their profiles.
- Search and list artists by **name, genre, or location**.

### Event Listings
- CRUD operations for **events** (Title, Date, Venue, Organizer, Ticket Price).
- Search events by **date, location, or artist**.

### Booking & Transactions
- Users can book **artists** for events.
- Manage booking statuses: **Pending, Confirmed, Completed**.
- Secure **payment processing** for artist bookings.

## Setup Instructions

### Prerequisites
- Python 3.9+
- PostgreSQL
- Virtual Environment (venv)

### Installation
```sh
# Clone the repository
git clone https://github.com/LmOpe/book-it.git
cd book-it

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\\Scripts\\activate'

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and set DATABASE_URL and other configurations

# Run database migrations
alembic upgrade head

# Start the server
uvicorn main:app --host 0.0.0.0 --port 7001 --reload
```

## API Documentation
Once the server is running, visit:
- Swagger UI: [http://localhost:7001/docs](http://localhost:7001/docs)
- ReDoc: [http://localhost:7001/redoc](http://localhost:7001/redoc)

## License
MIT License

