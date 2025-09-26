## ProDev Poll System

A backend-only polling system built with Django REST Framework. This project allows creating and managing polls, options, and votes, with JWT authentication for users and interactive API documentation using Swagger.

The project uses PostgreSQL for data persistence.

## Features

User Authentication

Register new users

JWT-based login (access & refresh tokens)

View and update profile

Poll Management

Create, update, soft-delete polls

Add multiple options per poll

Filter and search polls

Voting System

Users can cast votes (one vote per poll)

View results with counts and percentages

Cache-enabled for faster result retrieval

## API Documentation

Swagger (/swagger/) for interactive API testing

ReDoc (/redoc/) as alternative documentation

## Technologies Used

Backend: Python 3.x, Django, Django REST Framework

Authentication: Simple JWT

Database: PostgreSQL

API Documentation: drf-yasg (Swagger & ReDoc)

Containerization: Docker & Docker Compose

Caching: Django Cache Framework (Redis)

Setup Instructions
1. Clone the repository
git clone https://github.com/deenakamal/prodev-poll-system.git
cd prodev-poll-system

2. Environment Variables

A .env file is already included with the repository and contains the configuration required to run the project.

If you want to use your own environment variables, you can create your own .env file:

``` bash 
cp .env.example .env
```


Then update the values as needed:
``` env
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
SECRET_KEY=your_django_secret_key
DEBUG=True

```
Otherwise, the included .env file will be used automatically by Docker Compose.

3. Run with Docker Compose

The project is fully automated via Docker Compose. All required services (Django + PostgreSQL) will run, migrations will apply, initial data will load if needed, and the server will start automatically.

``` bash 
docker compose up --build
```


The Django server will be accessible at: http://localhost:8000

Admin panel: http://localhost:8000/admin/

Swagger UI: http://localhost:8000/swagger/

ReDoc UI: http://localhost:8000/redoc/

Note: A superuser can be created inside the running container if you need admin access:
``` bash
docker compose exec web python manage.py createsuperuser
```

## API Endpoints

### Users & Auth

| Route                  | HTTP Method | Description                           |
|------------------------|-------------|---------------------------------------|
| `/api/users/register/` | POST        | Register a new user                   |
| `/api/users/me/`       | GET         | Get current user profile              |
| `/api/users/me/`       | PUT         | Update current user profile           |
| `/api/token/`          | POST        | Obtain JWT access & refresh tokens   |
| `/api/token/refresh/`  | POST        | Refresh JWT access token              |

### Polls & Voting

| Route                              | HTTP Method | Description                                      |
|------------------------------------|-------------|--------------------------------------------------|
| `/api/polls/`                       | GET         | List all polls                                  |
| `/api/polls/`                       | POST        | Create a new poll (admin/creator only)         |
| `/api/polls/vote/`                  | POST        | Cast a vote (one vote per user per poll)       |
| `/api/polls/my-votes/`              | GET         | List polls the user has voted in               |
| `/api/polls/results/<poll_id>/`     | GET         | View poll results with vote counts & %        |

## Contributing

Fork the repository

Create a branch: git checkout -b feature-branch

Commit changes: git commit -am 'Add new feature'

Push branch: git push origin feature-branch

Open a pull request

## License

This project is licensed under the MIT License. See LICENSE for details.
