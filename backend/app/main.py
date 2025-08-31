from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.core.config import settings
from app.core.security import decode_access_token_raw
from app.routers import users, attractions, tickets, employees, reservations

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title = "EuroDisney API",
    description = "API de gestion pour EuroDisney",
    version = "1.0.0"
)

# CORS
if settings.BACKEND_CORS_ORIGINS:
    origins = [o.strip() for o in settings.BACKEND_CORS_ORIGINS.split(",")]
else:
    origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware: logs + user
@app.middleware("http")
async def log_requests(request: Request, call_next):
    auth = request.headers.get("Authorization", "")
    user = {"sub": "anonymous", "role": "guest"}
    if auth.startswith("Bearer "):
        token = auth.split(" ")[1]
        try:
            payload = decode_access_token_raw(token)
            user = {"sub": payload.get("sub"), "role": payload.get("role")}
        except Exception as e:
            logger.warning(f"Invalid token: {e}")
    logger.info(f"Request: {request.method} {request.url.path} - User: {user['sub']} - Role: {user['role']}")
    response = await call_next(request)
    logger.info(f"Request: {request.method} {request.url.path} - Status: {response.status_code}")
    return response


# Inclure les routers
app.include_router(users.router, prefix="/auth", tags=["auth"])
app.include_router(attractions.router, prefix="/attractions", tags=["attractions"])
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(reservations.router, prefix="/reservations", tags=["reservations"])

@app.get("/")
async def root():
    return {"message": "Welcome to EuroDisney API"}