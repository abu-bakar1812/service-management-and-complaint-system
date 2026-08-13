# Service Management and Complaint System

A backend-based Service Management and Complaint System built with **FastAPI** and **MongoDB Atlas**.

The system provides role-based access for **Customers, Agents, and Admins**. Customers can submit complaints, Admins can manage and assign complaints to Agents, and Agents can update the status of assigned complaints.

## Features

- User Registration and Login
- JWT Authentication
- Role-Based Authorization
- Customer Complaint Creation
- Customer Complaint Management
- Admin Complaint Management
- Admin Complaint Assignment to Agents
- Agent Assigned Complaint Management
- Complaint Status Updates
- MongoDB Atlas Database
- Swagger UI / OpenAPI Documentation
- Secure Password Hashing
- Environment Variables for Sensitive Configuration

## User Roles

### Customer

- Register and login
- Create complaints
- View own complaints
- Track complaint status

### Admin

- Manage complaints
- View complaints
- Assign complaints to agents
- Manage system operations

### Agent

- View assigned complaints
- Update complaint status
- Handle assigned customer complaints

## Technologies Used

- Python
- FastAPI
- MongoDB Atlas
- PyMongo
- JWT Authentication
- Pydantic
- Argon2 Password Hashing
- Swagger UI
- Uvicorn
- Git & GitHub

## Project Structure

```text
service-management-and-complaint-system/
│
├── main.py
├── database.py
├── schemas.py
├── dependencies.py
├── auth.py
├── pyproject.toml
├── uv.lock
├── .gitignore
│
└── router/
    ├── __init__.py
    ├── auth_router.py
    ├── complaint_router.py
    ├── admin_router.py
    └── agent_router.py