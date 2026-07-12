# Splitwise-like Expense Sharing Application using Specmatic

A **contract-first Expense Sharing Application** inspired by Splitwise, built using **FastAPI**, **OpenAPI 3.0**, and **Specmatic**.

This project demonstrates how executable API contracts eliminate integration uncertainty by serving as the **single source of truth** for developers, testers, CI pipelines, and AI coding agents.

---

# Objective

Traditional software development often suffers from integration issues because frontend and backend teams make assumptions about API behavior.

This project solves that problem using **Specmatic** by:

- Defining APIs as executable OpenAPI contracts
- Generating mock servers directly from API specifications
- Validating backend implementations through automated contract testing
- Performing schema resiliency testing
- Measuring API coverage
- Integrating contract validation into GitHub Actions CI/CD
- Supporting AI coding agents with precise executable specifications

---

# Tech Stack

- FastAPI
- Python 3.11
- OpenAPI 3.0
- Specmatic
- Docker
- GitHub Actions

---

# API Operations

## Groups

| Method | Endpoint |
|---------|----------|
| POST | /groups |
| GET | /groups/{groupId} |

## Expenses

| Method | Endpoint |
|---------|----------|
| POST | /expenses |
| GET | /expenses |

## Balances

| Method | Endpoint |
|---------|----------|
| GET | /balances/{userId} |

## Settlements

| Method | Endpoint |
|---------|----------|
| POST | /settlements |

## Actuator

| Method | Endpoint |
|---------|----------|
| GET | /actuator/mappings |

The custom actuator endpoint exposes all registered FastAPI routes using `app.routes` and is covered by Specmatic contract tests.

---

# Project Structure

```text
splitwise-specmatic-demo
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── services.py
│   ├── storage.py
│   └── requirements.txt
│
├── openapi/
│   └── expense-sharing-api.yaml
│
├── .github/
│   └── workflows/
│       └── specmatic.yml
│
├── specmatic-contract.yaml
├── specmatic-resiliency.yaml
└── README.md
```

---

# Contract-First Workflow

```
OpenAPI Contract
        │
        ▼
Specmatic Mock Server
        │
        ▼
FastAPI Implementation
        │
        ▼
Contract Testing
        │
        ▼
Schema Resiliency Testing
        │
        ▼
GitHub Actions CI/CD
        │
        ▼
Verified API Implementation
```

The OpenAPI specification acts as the **single source of truth** throughout development.

---

# Running the Backend

## Clone Repository

```bash
git clone https://github.com/jayeshpatil11/splitwise-specmatic-demo.git
cd splitwise-specmatic-demo
```

---

## Install Dependencies

```bash
cd backend

pip install -r requirements.txt
```

---

## Start FastAPI

```bash
uvicorn main:app --reload
```

Application

```
http://localhost:8000
```

Swagger UI

```
http://localhost:8000/docs
```

OpenAPI JSON

```
http://localhost:8000/openapi.json
```

---

# Custom Actuator Endpoint

The project includes a custom actuator endpoint similar to Spring Boot Actuator.

```
GET /actuator/mappings
```

It dynamically lists every registered FastAPI route using:

```python
app.routes
```

Example Response

```json
{
  "application": "expense-sharing-api",
  "framework": "FastAPI",
  "totalEndpoints": 7,
  "mappings": [
    {
      "path": "/groups",
      "methods": ["POST"],
      "name": "create_group"
    }
  ]
}
```

---

# Running Specmatic Mock Server

```bash
MSYS_NO_PATHCONV=1 docker run --rm \
-v ${PWD}:/workspace \
-w /workspace \
specmatic/specmatic:latest \
mock openapi/expense-sharing-api.yaml
```

Specmatic automatically generates mock APIs from the OpenAPI contract.

---

# Running Contract Tests

Start the FastAPI application first.

Then execute:

```bash
MSYS_NO_PATHCONV=1 docker run --rm \
-v ${PWD}:/workspace \
-w /workspace \
--add-host=host.docker.internal:host-gateway \
specmatic/specmatic:latest \
test \
--config specmatic-contract.yaml \
--testBaseURL=http://host.docker.internal:8000
```

Contract testing validates:

- Request schemas
- Response schemas
- Status codes
- Required fields
- Data types
- OpenAPI examples

---

# Running Schema Resiliency Tests

```bash
MSYS_NO_PATHCONV=1 docker run --rm \
-v ${PWD}:/workspace \
-w /workspace \
--add-host=host.docker.internal:host-gateway \
specmatic/specmatic:latest \
test \
--config specmatic-resiliency.yaml \
--testBaseURL=http://host.docker.internal:8000
```

Schema resiliency testing automatically generates negative scenarios including:

- Missing request body
- Missing required fields
- Invalid path parameters
- Null values
- Wrong data types
- Boolean instead of integer
- String instead of number

---

# Contract Test Results

✅ **12 / 12 Tests Passed**

- 100% API Coverage
- No Contract Violations

---

# Schema Resiliency Test Results

✅ **41 / 41 Tests Passed**

Automatically generated positive and negative scenarios validated successfully.

---

# GitHub Actions CI/CD

Every push and pull request automatically performs:

- Install Dependencies
- Start FastAPI Server
- Run Contract Tests
- Run Schema Resiliency Tests
- Generate Separate Test Reports
- Upload Reports as GitHub Artifacts

The CI pipeline maintains **separate jobs** for:

- Contract Testing
- Schema Resiliency Testing

---

# Example API

## Create Group

Request

```json
{
  "name": "Goa Trip"
}
```

Response

```json
{
  "groupId": 1,
  "name": "Goa Trip"
}
```

---

# Why Specmatic?

Specmatic transforms OpenAPI specifications into executable contracts.

Benefits include:

- Contract-first development
- Automated API validation
- Instant mock generation
- Schema resiliency testing
- API coverage reports
- GitHub Actions integration
- Better collaboration
- Reduced integration failures

---

# How This Helps AI Coding Agents

Without executable contracts, AI coding assistants infer API behavior.

With Specmatic, AI receives:

- Endpoint definitions
- Request schemas
- Response schemas
- Validation rules
- Executable examples
- API behavior

This significantly reduces ambiguity and improves generated code quality.

---

# Key Learnings

Through this project I learned:

- Contract-first API development
- OpenAPI specification design
- FastAPI implementation
- Specmatic Contract Testing
- Schema Resiliency Testing
- API Coverage Analysis
- GitHub Actions CI/CD
- Custom Actuator implementation
- OpenAPI example management
- AI-assisted development using executable contracts

---

# Project Achievements

- ✅ Contract-First Development
- ✅ FastAPI Backend
- ✅ OpenAPI 3.0 Specification
- ✅ Custom Actuator Endpoint
- ✅ Specmatic Contract Testing
- ✅ Schema Resiliency Testing
- ✅ 100% API Coverage
- ✅ 41/41 Resiliency Tests Passed
- ✅ GitHub Actions CI/CD
- ✅ Executable API Contracts

---

# Future Enhancements

- JWT Authentication
- User Management
- Group Membership APIs
- Equal and Unequal Expense Splitting
- Settlement History
- PostgreSQL/MySQL Integration
- Docker Compose Support
- Kubernetes Deployment
- Microservices Architecture
- Monitoring and Logging

---
