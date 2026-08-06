#  CloudBox

CloudBox is a secure cloud file storage backend built using FastAPI. It provides JWT-based authentication, AWS S3 file storage, PostgreSQL metadata management, and Dockerized deployment.

---

## Features

- User Registration & Login
- JWT Authentication
- Secure Password Hashing
- Upload Files to AWS S3
- Download Files using Presigned URLs
- Delete Files
- PostgreSQL Database
- Docker & Docker Compose Support

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- AWS S3
- JWT
- Docker
- Docker Compose
- Boto3

---

## Project Structure

```text
app/
│
├── core/
├── crud/
├── db/
├── models/
├── routers/
├── schemas/
├── services/
└── main.py
```

---

# 🏗️ Architecture

```text
                    +------------------+
                    |      Client      |
                    +------------------+
                             |
                             | HTTP Requests
                             ▼
                    +------------------+
                    |     FastAPI      |
                    |   REST Backend   |
                    +------------------+
                             |
          +------------------+------------------+
          |                                     |
          ▼                                     ▼
+------------------------+          +------------------------+
|     PostgreSQL DB      |          |       AWS S3 Bucket    |
|                        |          |                        |
| User Information       |          | Uploaded Files        |
| File Metadata          |          | PDFs, Images, Docs    |
| Authentication Data    |          | Secure Object Storage |
+------------------------+          +------------------------+
```

---


## Installation

```bash
git clone <repo-url>

cd CloudBox

cp .env.example .env

docker compose up --build
```

---

## API Endpoints

### Authentication

POST /auth/register

POST /auth/login

---

### Files

POST /files/upload

GET /files

GET /files/{id}/download

DELETE /files/{id}/delete

---

## Future Improvements

- Folder support
- File sharing
- Password Reset
- Email Verification
- CI/CD Pipeline
- Deployment on AWS EC2
  
---

## Author

Harshita Sharma
