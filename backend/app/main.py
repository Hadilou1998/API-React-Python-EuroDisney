from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.routers import users, attractions, tickets, employees, reservations

# App
app = FastAPI(
    title="EuroDisney API",
    description="API de gestion pour EuroDisney",
    version="1.0.0"
)

# CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # IMPORTANT pour avec credentials
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware simple pour logs + JWT
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    return response

# Routers
app.include_router(users.router, prefix="/auth", tags=["auth"])
app.include_router(attractions.router, prefix="/attractions", tags=["attractions"])
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(reservations.router, prefix="/reservations", tags=["reservations"])

@app.get("/")
async def root():
    return {"message": "Welcome to EuroDisney API"}

@app.get("/health")
async def health():
    return {"status": "OK", "message": "API is running"}