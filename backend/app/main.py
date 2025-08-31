from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.core.config import settings
from app.core.security import decode_access_token_raw
from app.routers import users, attractions, tickets, employees, reservations

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# App
app = FastAPI(
    title="EuroDisney API",
    description="API de gestion pour EuroDisney",
    version="1.0.0"
)

# CORS
origins = ["http://localhost:5173"]  # frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # IMPORTANT pour avec credentials
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware pour logs et JWT
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

# Routers
app.include_router(users.router, prefix="/auth", tags=["auth"])
app.include_router(attractions.router, prefix="/attractions")
app.include_router(tickets.router, prefix="/tickets")
app.include_router(employees.router, prefix="/employees")
app.include_router(reservations.router, prefix="/reservations")

@app.get("/")
async def root():
    return {"message": "Welcome to EuroDisney API"}