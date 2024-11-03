

# BookTrade Backend Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Tech Stack](#tech-stack)
4. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Environment Variables](#environment-variables)
5. [Database Schema](#database-schema)
6. [API Documentation](#api-documentation)
   - [Authentication](#authentication)
   - [Endpoints](#endpoints)
7. [Error Handling](#error-handling)
8. [Deployment](#deployment)
9. [Security](#security)

---

## 1. Project Overview

BookTrade is a platform for users to exchange books. The backend supports user authentication, book listing, searching, and exchanging, as well as messaging and transaction management. Key features include:
- User authentication with OTP-based registration.
- CRUD operations for books.
- Messaging system between users for exchange requests.
- Notifications for transaction updates.

## 2. System Architecture

BookTrade’s backend follows a monolithic architecture using Django with Django REST Framework. The backend connects to a PostgreSQL database, with Firebase Storage used for book images and Gmail SMTP for OTP-based email verification.

### Architecture Diagram 
- **Django REST Framework** serves the REST API.
- **PostgreSQL** stores user, book, and transaction data.
- **Firebase Storage** for storing and retrieving book images.
- **Gmail SMTP** for OTP-based user authentication emails.

![alt text](AD.png "Title")

## 3. Tech Stack

- **Framework**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT for session management
- **Storage**: Firebase Storage (for images)
- **Email Service**: Gmail SMTP (for OTP verification)

## 4. Getting Started

### Prerequisites

- **Python**: v3.8+
- **PostgreSQL**: v12+
- **Firebase Storage**: Firebase account and project setup
- **Gmail**: Gmail account for SMTP

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sayanlp99/booktrade-backend.git
   cd booktrade-backend
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL**
   ```sql
   CREATE DATABASE booktrade_db;
   CREATE USER booktrade_user WITH PASSWORD 'password';
   ALTER ROLE booktrade_user SET client_encoding TO 'utf8';
   ALTER ROLE booktrade_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE booktrade_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE booktrade_db TO booktrade_user;
   ```

4. **Apply Django migrations**
   ```bash
   python manage.py migrate
   ```

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DB_NAME=booktrade_db
DB_USER=booktrade_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=your_secret_key
DEBUG=True

# Firebase
FIREBASE_STORAGE_BUCKET=your_firebase_bucket

# Gmail SMTP
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password

# JWT
JWT_SECRET_KEY=your_jwt_secret_key
```

## 5. Database Schema

The database includes the following key tables:

- **User**: Stores user details including authentication data and profile information.
- **Book**: Stores book listings with details such as title, author, genre, and Firebase Storage link for images.
- **Transaction**: Tracks book exchanges and user requests.
- **Messages**: Manages communication between users during an exchange request.

Refer to the `database_schema.png` for an ERD of the schema.

## 6. API Documentation

### Authentication

BookTrade uses JWT-based authentication with OTP verification for user registration.

- **Register**: `/api/auth/register/` - Sends an OTP to the user’s email.
- **Verify OTP**: `/api/auth/verify-otp/` - Verifies the OTP and completes registration.
- **Login**: `/api/auth/login/` - Issues JWT for subsequent requests.
- **Protected Routes**: JWT required in `Authorization` header for access.

### Endpoints

| Method | Endpoint                  | Description                            |
|--------|----------------------------|----------------------------------------|
| POST   | `/api/auth/register/`      | Sends OTP for user registration        |
| POST   | `/api/auth/verify-otp/`    | Verifies OTP to complete registration  |
| POST   | `/api/auth/login/`         | Authenticates user and returns JWT     |
| GET    | `/api/books/`              | Retrieves list of available books      |
| POST   | `/api/books/`              | Adds a new book                        |
| GET    | `/api/books/{id}/`         | Retrieves details of a specific book   |
| PATCH  | `/api/books/{id}/`         | Updates details of a specific book     |
| DELETE | `/api/books/{id}/`         | Deletes a specific book                |
| POST   | `/api/exchanges/`          | Initiates an exchange request          |
| GET    | `/api/exchanges/{id}/`     | Retrieves status of exchange request   |
| POST   | `/api/messages/`           | Sends message related to exchange      |


## 7. Error Handling

Errors are returned in the following JSON structure:

```json
{
  "error": {
    "code": 400,
    "message": "Validation failed",
    "details": {
      "field": "Error details here"
    }
  }
}
```

### Common Error Codes

- **400**: Bad Request - Validation errors or malformed data.
- **401**: Unauthorized - Invalid or missing JWT.
- **404**: Not Found - Resource does not exist.
- **500**: Internal Server Error - Generic server error.


## 8. Deployment

To run the BookTrade backend locally, use the following command:

```bash
python manage.py runserver 0.0.0.0:8000
```

This command starts the Django development server, making your API accessible at `http://<your-ip>:8000`.

Make sure to replace `<your-ip>` with your server's actual IP address if you're deploying on a remote server. For local development, you can use `localhost` or `127.0.0.1`.

---

## 9. Security

- **JWT Authentication**: Secures endpoints with token-based authentication.
- **CORS**: Configured to allow only specific origins.
- **Sensitive Data Encryption**: Passwords are encrypted using Django’s `make_password` function.
- **Rate Limiting** (if applicable): Configured to prevent abuse.

--- 
