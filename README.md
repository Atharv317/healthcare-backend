# Healthcare Backend

A RESTful healthcare backend built with Django, Django REST Framework, PostgreSQL, and JWT authentication.

## Features

* User registration and login using email and password
* JWT-based authentication
* JWT access-token refresh
* Patient management with user-based ownership
* Doctor management with owner-based update/delete authorization
* Patient-doctor mapping
* Duplicate mapping prevention
* Request validation and permission handling
* PostgreSQL database integration
* Django admin support
* Automated API tests

## Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* djangorestframework-simplejwt
* psycopg
* python-dotenv

## Project Structure

```text
healthcare-backend/
│
├── accounts/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── doctors/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── mappings/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── patients/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── .env.example
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Atharv317/healthcare-backend.git
cd healthcare-backend
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database for the project.

Example:

```text
Database: healthcare_db
User: postgres
Host: localhost
Port: 5432
```

### 5. Configure environment variables

Create a `.env` file in the project root based on `.env.example`.

Example:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your-postgres-password
DB_HOST=localhost
DB_PORT=5432
```

Do not commit `.env` to version control.

### 6. Apply migrations

```powershell
python manage.py migrate
```

### 7. Create an admin user

```powershell
python manage.py createsuperuser
```

### 8. Start the development server

```powershell
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## Authentication

### Register

```http
POST /api/auth/register/
```

Request:

```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "StrongPassword123!"
}
```

### Login

```http
POST /api/auth/login/
```

Request:

```json
{
    "email": "john@example.com",
    "password": "StrongPassword123!"
}
```

The response contains an access token and a refresh token.

For protected endpoints, send:

```http
Authorization: Bearer <access_token>
```

### Refresh Access Token

```http
POST /api/auth/token/refresh/
```

Request:

```json
{
    "refresh": "<refresh_token>"
}
```

### Current User

```http
GET /api/auth/me/
```

Requires authentication.

## Patient APIs

All patient endpoints require authentication.

### Create Patient

```http
POST /api/patients/
```

### List Own Patients

```http
GET /api/patients/
```

Returns patients created by the authenticated user.

### Get Patient

```http
GET /api/patients/<id>/
```

### Update Patient

```http
PUT /api/patients/<id>/
```

### Delete Patient

```http
DELETE /api/patients/<id>/
```

Users can only access and manage their own patient records.

## Doctor APIs

All doctor endpoints require authentication.

### Create Doctor

```http
POST /api/doctors/
```

### List Doctors

```http
GET /api/doctors/
```

Returns all doctors.

### Get Doctor

```http
GET /api/doctors/<id>/
```

### Update Doctor

```http
PUT /api/doctors/<id>/
```

### Delete Doctor

```http
DELETE /api/doctors/<id>/
```

All authenticated users can view doctors. Only the user who created a doctor can update or delete that doctor.

## Patient-Doctor Mapping APIs

All mapping endpoints require authentication.

### Create Mapping

```http
POST /api/mappings/
```

Request:

```json
{
    "patient": 1,
    "doctor": 1
}
```

### List Mappings

```http
GET /api/mappings/
```

Returns mappings for patients owned by the authenticated user.

### Get Doctors Assigned to a Patient

```http
GET /api/mappings/<patient_id>/
```

Returns the doctors assigned to the specified patient.

The authenticated user can only retrieve mappings for their own patients.

### Delete Mapping

```http
DELETE /api/mappings/<id>/
```

Removes the specified patient-doctor mapping.

Duplicate patient-doctor assignments are prevented using both serializer validation and a database-level unique constraint.

## Validation and Error Handling

The API uses Django REST Framework validation and permission handling.

Common responses include:

* `400 Bad Request` — invalid request data
* `401 Unauthorized` — authentication required or invalid
* `403 Forbidden` — authenticated user does not have permission
* `404 Not Found` — requested resource does not exist or is not accessible

Password validation uses Django's configured password validators.

## Database

The application uses PostgreSQL through Django's ORM.

Database credentials are loaded from environment variables rather than being hard-coded in the source code.

## Testing

Run the complete automated test suite:

```powershell
python manage.py test
```

The project includes tests covering:

* User registration
* Duplicate email registration
* Login
* Invalid login
* JWT authentication requirements
* JWT refresh
* Patient creation and ownership
* Patient access restrictions
* Doctor creation and retrieval
* Doctor owner permissions
* Patient-doctor mapping creation
* Duplicate mapping prevention
* Mapping ownership
* Mapping retrieval
* Mapping deletion

## Django Admin

After creating a superuser:

```powershell
python manage.py createsuperuser
```

Open:

```text
http://127.0.0.1:8000/admin/
```

The admin interface provides access to users, patients, doctors, and patient-doctor mappings.

## Development Checks

Before submission, run:

```powershell
python manage.py check
python manage.py test
```

Both commands should complete successfully without errors.

## Security Notes

* Secret configuration is stored in environment variables.
* `.env` is excluded from version control.
* Passwords are hashed using Django's authentication system.
* Protected endpoints require JWT authentication.
* Patient records are isolated by their creator.
* Doctor modifications are restricted to the doctor creator.
* Patient-doctor mappings enforce patient ownership.
* Duplicate patient-doctor mappings are prevented at the database level.
