# Customer Order Management API
This repository contains the source code for a RESTful API service built with Django for managing customers and their orders. The API is designed to handle CRUD operations for customers and orders, and it also integrates with OpenID Connect for authentication and SMS notifications via Africa's Talking.

## Project Structure
The project follows a standard Django project structure:
```bash
customer_order_service/
├── .github
│   └── workflows
│       └── ci-cd.yml
├── orders
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── customer_order_service
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── Customer Order.postman_collection.json
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── manage.py
└── requirements.txt
```

## Features

- Customer management (CRUD operations)
- Order management with real-time SMS notifications
- OpenID Connect Authentication
- REST API endpoints
- Automated testing with high coverage
- CI/CD pipeline integration

## Tech Stack

- Python 3.x
- Django & Django REST Framework
- DbSqlite
- Africa's Talking SMS Gateway
- OpenID Connect for authentication
- Docker
- GitHub Actions (CI/CD)

## Prerequisites

- Python 3.x
- DbSqlite
- Docker (optional)
- Africa's Talking Account
- OpenID Connect Provider credentials

## Installation

1. Clone the repository
```bash
git clone (Current Repo)[https://github.com/TangoIndiaMango/sa_customer_order]
cd sa_interview_order
```
2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Set up environment variables
```bash
cp .env.example .env
```
5. Run migrations
```bash
python manage.py migrate
```
6. Start development server
```bash
python manage.py runserver
```

### OR
```bash
./start.sh
```

## API Endpoints
### Authentication
- POST /auth/registration/ - Create User
- POST /auth/login/ - Login User
### Customers
- GET /api/customers/ - List all customers
- POST /api/customers/ - Create a new customer
- GET /api/customers/{id}/ - Retrieve a customer
- PUT /api/customers/{id}/ - Update a customer
- DELETE /api/customers/{id}/ - Delete a customer
### Orders
- GET /api/orders/ - List all orders
- POST /api/orders/ - Create a new order
- GET /api/orders/{id}/ - Retrieve an order
- PUT /api/orders/{id}/ - Update an order
- DELETE /api/orders/{id}/ - Delete an order

## Authentication
This API uses OpenID Connect for authentication. To access protected endpoints:

Obtain an access token from the authentication endpoint
Include the token in the Authorization header:
plaintext

Authorization: Bearer <your-token>
SMS Notifications
The system automatically sends SMS notifications to customers when new orders are created using Africa's Talking SMS gateway.

Testing
Run the test suite:
```bash
python manage.py test
```

### CI/CD
This project uses GitHub Actions for CI/CD. The pipeline:

Runs tests
Checks code coverage
Performs linting
Deploys to production on successful merge to main branch

## Docker Deployment

### Build the Docker image locally
```bash
docker build -t customer-order-service .
```

### Prerequisites
- Docker

### Build and Push Docker Image
```bash
docker build -t your-registry/customer-order-service:latest .
docker push your-registry/customer-order-service:latest
```