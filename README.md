# Car Parking Backend API (No Authentication)

This repository contains the backend implementation for a Car Parking System API built using Flask and PostgreSQL. It provides endpoints to manage parking lot information, user data, and parking sessions.

**Note:** This implementation currently does not include user authentication.

## Table of Contents

* [Features](#features)
* [Technology Stack](#technology-stack)
* [Prerequisites](#prerequisites)
* [Installation & Setup](#installation--setup)
    * [Clone Repository](#1-clone-repository)
    * [Create Virtual Environment](#2-create-virtual-environment-recommended)
    * [Install Dependencies](#3-install-dependencies)
    * [Database Setup](#4-database-setup)
    * [Database Configuration](#5-database-configuration)
* [Running the Application](#running-the-application)
* [API Endpoints](#api-endpoints)
* [Database Schema](#database-schema)
* [Testing](#testing)
* [Contributing](#contributing)
* [License](#license)

## Features

* Retrieve details of all parking lots.
* View the structure of the parking lot (Floors, Rows, Slots - *endpoint implementation needed*).
* Manage user information (Create, Read, Update).
* Park a vehicle in an available slot (*endpoint implementation needed*).
* Remove a vehicle from a slot using a ticket ID (*endpoint implementation needed*).
* View parking session details (*endpoint implementation needed*).

## Technology Stack

* **Framework:** Flask
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Language:** Python

## Prerequisites

Before you begin, ensure you have the following installed:

* Python 3.x
* pip (Python package installer)
* PostgreSQL Server

## Installation & Setup

Follow these steps to get the project running locally:

### 1. Clone Repository

```bash
git clone https://github.com/veenayaksirohi/No_Auth_Backend-Implementation-for-Car-Parking-Project.git
cd No_Auth_Backend-Implementation-for-Car-Parking-Project
```

### 2. Create Virtual Environment (Recommended)
```bash
# For Linux/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```sql
-- Ensure your PostgreSQL server is running
-- Create database using psql
CREATE DATABASE parking_db;

-- Restore database
psql -U <your_postgres_username> -d parking_db -f parking_backup.sql  # "(parking_backup.sql file location )"
```

### 5. Database Configuration
The database connection details are currently set directly in app.py:

```python
# Inside create_app() in app.py
username = "postgres"
password = urllib.parse.quote_plus("root") # URL encodes the password
host = "localhost"
port = 5432
database_name = "parking_db"
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@{host}:{port}/{database_name}"
```

Important: For security and flexibility, it's highly recommended to modify this to use environment variables instead of hardcoding credentials. Update the username, password, host, and port variables to match your local PostgreSQL setup if they differ from the defaults.

## Running the Application

Once the setup is complete, you can run the Flask application using the run.py script:

```bash
python run.py
```

The application should now be running, typically on http://127.0.0.1:5000/.

## API Endpoints

The following endpoints are available:

| Method | Path | Description | Request Body (JSON) | Response |
|--------|------|-------------|---------------------|----------|
| GET | / | Welcome page with links to other GET endpoints. | N/A | HTML page |
| GET | /parkinglots_details | Get details of all parking lots. | N/A | JSON array of parking lot objects |
| GET | /parking_lot | Get the structure (Floors, Rows, Slots). | N/A | JSON (Structure depends on implementation) |
| GET | /users | Get a list of all registered users. | N/A | JSON array of user objects |
| POST | /users | Create a new user. | See User model | JSON of the created user or error message |
| PUT | /users/<user_id> | Update an existing user by ID. | See User model | JSON of the updated user or error message |
| POST | /park_car | Park a car in an available slot. | Requires details | Requires details |
| DELETE | /remove_car_by_ticket | Remove a parked car using its ticket ID. | Requires details | Requires details |

(Note: Endpoints marked with "Requires details" need further implementation or clarification on request/response formats based on the full code.)

## Database Schema

The application uses several SQLAlchemy models mapped to PostgreSQL tables:

* ParkingData: Stores general information about different parking locations.
* Parkinglots_Details: Seems similar to ParkingData, potentially redundant or for a different purpose (clarification needed).
* Floor: Represents a floor within a parking structure.
* Row: Represents a row of parking slots on a specific floor.
* Slot: Represents an individual parking slot, including its status and occupant details.
* User: Stores information about registered users.
* Reservation: Manages pre-booked reservations for slots (implementation details needed).
* ParkingSession: Tracks active parking sessions, linking vehicles to slots and users.

Refer to app.py for detailed model definitions and parking_backup.sql for the exact table structure.

## Testing

The repository includes a test_app.py file. To run the tests:

```bash
# Ensure you have pytest installed
pip install pytest
pytest test_app.py
```

(Note: Test coverage and specific test commands might need adjustment based on the actual test setup in test_app.py.)

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/your-feature-name).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (git push origin feature/your-feature-name).
6. Open a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
