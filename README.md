# Campaigns API (FastAPI Version)

A REST API for managing **marketing campaigns**.
Originally designed as a .NET backend assessment, this implementation uses **FastAPI**, **SQLAlchemy**, and **JWT authentication** to replicate the required functionality.

---

## Features

* Campaign CRUD operations (Create, Read, Update, Delete)
* Validation for campaign fields
* JWT-based authentication
* Pagination, filtering, and sorting
* Swagger (OpenAPI) documentation at `/docs`
* Unit and integration tests with `pytest`
* Database persistence via SQLAlchemy ORM
* Alembic migrations (optional)
* Ready for deployment to Render, Railway, or any cloud provider

---

## Tech Stack

* **FastAPI** — Web Framework
* **SQLAlchemy** — ORM for data models
* **PostgreSQL / SQLite** — Database
* **Pydantic v2** — Data validation
* **JWT (PyJWT / python-jose)** — Authentication
* **Alembic** — Database migrations
* **Pytest** — Testing framework

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/<hezzy93>/campaigns_api.git
cd campaigns_api
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate     # On macOS/Linux
venv\Scripts\activate        # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup environment variables

Create a `.env` file in the root directory and add:

```env
DATABASE_URL=sqlite:///./campaigns.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run database migrations (if using Alembic)

```bash
alembic upgrade head
```

### 6. Start the development server

```bash
uvicorn main:app --reload
```

The API will be available at:
`http://127.0.0.1:8000`

Swagger docs:
`http://127.0.0.1:8000/docs`

---

## Running Tests

To execute unit and integration tests:

```bash
pytest -v
```

All tests should pass.

---

## Example Endpoints

| Method | Endpoint                     | Description                    |
| ------ | ---------------------------- | ------------------------------ |
| POST   | `/api/campaigns/`            | Create a new campaign          |
| GET    | `/api/campaigns/`            | List campaigns with pagination |
| GET    | `/api/campaigns/{campaign_id}`        | Retrieve a campaign by ID      |
| PUT    | `/api/campaigns/{campaign_id}`        | Update a campaign              |
| DELETE | `/api/campaigns/{campaign_id}` | Delete a campaign              |
| POST   | `/users/enroll`             | Register a user                |
| POST   | `/users_Login/`              | Login to get JWT token         |

---

## Folder Structure

```
campaigns_api/
│
├── main.py                # FastAPI entry point
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── crud.py                # Database operations
├── auth.py                # JWT authentication & password hash
│
├── tests/                 # Unit and integration tests
├── requirements.txt        # Python dependencies
├── alembic/                # Database migrations
├── .env                    # Environment variables
└── README.md               # Project documentation
```

---

## License

MIT License — free to use and modify.
