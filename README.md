# SecureAuth — DevSecOps Practice Project

A minimal JWT authentication app: FastAPI backend + vanilla HTML/JS frontend, containerised and ready for a CI/CD pipeline.

## Stack

| Layer    | Tech                          |
|----------|-------------------------------|
| Backend  | Python 3.12, FastAPI, SQLite  |
| Auth     | JWT (python-jose), bcrypt     |
| Frontend | HTML, CSS, vanilla JS         |
| Serve    | nginx (frontend container)    |
| CI       | GitHub Actions                |

## Quick start (Docker)

```bash
cp backend/.env.example backend/.env
# Edit backend/.env and set a real SECRET_KEY

docker compose up --build
```

- Frontend → http://localhost:3000  
- Backend API docs → http://localhost:8000/docs

## Quick start (local dev, no Docker)

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload

# Frontend (separate terminal — any static file server works)
cd frontend
python -m http.server 3000
```

## Run tests

```bash
cd backend
pytest test_main.py -v
```

## API endpoints

| Method | Path        | Auth required | Description          |
|--------|-------------|---------------|----------------------|
| POST   | /register   | No            | Create account       |
| POST   | /login      | No            | Returns JWT          |
| GET    | /me         | Yes (Bearer)  | Current user info    |
| GET    | /health     | No            | Health check for CI  |

## CI/CD pipeline (extend this as you go)

The `.github/workflows/ci.yml` skeleton already runs tests and Docker builds on push.  
Commented-out steps show where to add:

- Trivy for dependency/image vulnerability scanning  
- Gitleaks for secret detection  
- GHCR for image publishing  
- Deployment step (ECS, EKS, or App Runner)

## Project structure

```
auth-app/
├── backend/
│   ├── main.py            # FastAPI routes
│   ├── auth.py            # JWT + password helpers
│   ├── database.py        # SQLite connection
│   ├── models.py          # Pydantic schemas
│   ├── test_main.py       # Pytest tests
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── index.html         # Login + Register
│   ├── dashboard.html     # Protected page
│   ├── style.css
│   ├── app.js
│   └── Dockerfile
├── .github/workflows/ci.yml
├── docker-compose.yml
└── .gitignore
```
