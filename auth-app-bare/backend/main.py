import sqlite3

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from auth import create_access_token, decode_token, hash_password, verify_password
from database import get_connection, init_db
from models import LoginRequest, MessageResponse, RegisterRequest, TokenResponse, UserResponse

app = FastAPI(title="Auth API", version="1.0.0", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bearer = HTTPBearer()


@app.on_event("startup")
def startup() -> None:
    init_db()


# ── Auth routes ──────────────────────────────────────────────────────────────

@app.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest):
    if len(body.password) < 8:
        raise HTTPException(status_code=422, detail="Password must be at least 8 characters")
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (email, hashed_password) VALUES (?, ?)",
            (body.email, hash_password(body.password)),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Email already registered")
    finally:
        conn.close()
    return {"message": "Account created successfully"}


@app.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (body.email,)).fetchone()
    conn.close()

    if not row or not verify_password(body.password, row["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(row["id"]), "email": row["email"]})
    return {"access_token": token}


# ── Protected routes ─────────────────────────────────────────────────────────

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    try:
        return decode_token(credentials.credentials)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@app.get("/me", response_model=UserResponse)
def get_me(user: dict = Depends(get_current_user)):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user["sub"],)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": row["id"], "email": row["email"], "created_at": row["created_at"]}


# ── Health check (for CI/CD pipeline probes) ─────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "service": "auth-api"}
