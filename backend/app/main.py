import logging
import os

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.database import Base, engine, SessionLocal
from app.models import User
from app.routers import users, attractions, tickets, employees, reservations
from app.seed import seed

# App
app = FastAPI(
    title="EuroDisney API",
    description="API de gestion pour EuroDisney",
    version="1.0.0"
)

# Database startup event
@app.on_event("startup")
def startup_database():
    # En local, on continue d'utiliser MySQL/XAMPP normalement.
    if not os.getenv("VERCEL"):
        return

    # Sur Vercel, création de la base SQLite dans /tmp.
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Vérifier si la base est vide.
        database_is_empty = db.query(User).first() is None
    finally:
        db.close()

    # Si la base est vide, on seed.
    if database_is_empty:
        seed()

# CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://api-react-python-euro-disney.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # IMPORTANT pour avec credentials
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gestionnaire d'exception pour maintenir CORS en cas d'erreur 500
@app.exception_handler(Exception)
async def core_exception_handler(request: Request, exc: HTTPException):
    # Maintenir CORS même en cas d'erreur
    origin = request.headers.get("origin", "")
    headers = {}
    if origin in origins:
        headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }

    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
        headers=headers
    )

# Middleware simple pour logs + JWT
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url.path}")
    try:
        response = await call_next(request)
    except Exception as e:
        logging.error(f"Error during request: {e}", exc_info=True)
        origin = request.headers.get("origin", "")
        headers = {}
        if origin in origins:
            headers = {
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Credentials": "true"
            }
        response = JSONResponse(
            status_code=500,
            content={"detail": "Request failed"},
            headers=headers
        )       
    return response

# Routers
app.include_router(users.router, prefix="/api/auth", tags=["auth"])
app.include_router(attractions.router, prefix="/api/attractions", tags=["attractions"])
app.include_router(tickets.router, prefix="/api/tickets", tags=["tickets"])
app.include_router(employees.router, prefix="/api/employees", tags=["employees"])
app.include_router(reservations.router, prefix="/api/reservations", tags=["reservations"])

@app.get("/")
async def root():
    return {"message": "Welcome to EuroDisney API"}

@app.get("/api/health")
async def health():
    return {"status": "OK", "message": "API is running"}