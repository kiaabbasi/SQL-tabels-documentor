## My FastAPI Project ##

## This is a FastAPI project skeleton. ##

fum-fastapi-skeleton/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── items.py
│   │   │   │   ├── users.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py
│   │   ├── base.py
│   │   ├── schemas/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── item.py
│   │   │   │   ├── user.py
│   │   ├── repositories/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── item.py
│   │   │   ├── user.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logging.py
├── tests/
│   ├── __init__.py
│   ├── test_items.py
│   ├── test_users.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
├── README.md


Explanation of the Structure

app/main.py: The entry point of the application. This is where the FastAPI app is initialized and where you include your routers.

app/api/: This directory contains all the API-related code. It is further divided into:

v1/: Version 1 of your API. You can add more versions (e.g., v2/) as your API evolves.

endpoints/: Contains the route handlers for your API endpoints.

app/core/: Contains core configurations, security utilities, and other shared functionality.

config.py: Configuration settings (e.g., environment variables).

security.py: Security-related utilities (e.g., authentication, password hashing).

app/db/: Contains database-related code.

session.py: Database session management.

models/: SQLAlchemy models for database tables.

schemas/: Contains SQLAlchemy models (if you're using a database).

app/utils/: Utility functions and helpers (e.g., logging, custom validators).

tests/: Contains unit and integration tests for your API.

requirements.txt: Lists all Python dependencies.

Dockerfile and docker-compose.yml: For containerizing your application.

.env: Environment variables (e.g., database credentials, secret keys).

.gitignore: Specifies files and directories to ignore in version control.

By using __init__ everywhere, we can access the variables from the all over the app.


How to run dockerfile:

docker build -t fum-fastapi-skeleton .
docker run -itd  --name fum-fastapi-skeleton -p 8000:8000  fum-fastapi-skeleton



API calls:

curl -X GET "http://localhost:8000/api/v1/users/" -H "Content-Type: application/json"
output: [{"name":"test","email":"test","id":1},{"name":"tttt","email":"rrrrr","id":2}]

curl -X GET "http://localhost:8000/api/v1/users/1" -H "Content-Type: application/json"
output: {"email":"test","name":"test","id":1}

curl -X PUT "http://localhost:8000/api/v1/users/1" -H "Content-Type: application/json" -d '{
    "name": "tuser",
    "email": "tuser@example.com"
}'
output: {"name":"tuser","email":"tuser@example.com","id":1}

curl -X DELETE "http://localhost:8080/api/v1/users/2" -H "Content-Type: application/json" 
output: {"name":"tttt","email":"rrrrr","id":2}

curl -X POST "http://localhost:8000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "name": "new_user",
    "email": "new_user@example.com"
}'
output: {"name":"new_user","email":"new_user@example.com","id":3}       

Call Apis with header:

curl -X GET "http://127.0.0.1:8080/api/v1/users/10" \
-H "SYS-KEY: 123456" \
-H "PERSON-ID: 12" \
-H "USER-ROLES: 45" \
-H "IP-ADDRESS: 123.456.789.0" \
-H "USER-ID: 9422099160"



In app/db/session, some event listeners are added to log all the queries sent to the database along with their execution status.
