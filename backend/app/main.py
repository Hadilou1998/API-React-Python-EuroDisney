from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from app.core.config import settings
from app.core.security import decode_access_token_optional
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
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # IMPORTANT pour avec credentials
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Gestion des erreurs pour maintenir CORS meme sur les erreurs 500
@app.exception_handler(Exception)
async def cors_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error: {exc}")

    response = JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )

    # Ajout de l'en-tête Access-Control-Allow-Origin si l'origine est dans la liste des origines autorisées
    origin = request.headers.get("origin")
    if origin in origins:
        response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET", "POST", "PUT", "DELETE", "OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"

    return response

# Middleware pour logs et JWT - APRÈS CORS
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Skip pour OPTIONS déjà traité
    if request.method == "OPTIONS":
        return await call_next(request)
    
    auth = request.headers.get("Authorization", "")
    user = {"sub": "anonymous", "role": "guest"}

    if auth.startswith("Bearer "):
        token = auth.split(" ")[1]
        try:
            payload = decode_access_token_optional(token)
            if payload:
                user = {"sub": payload.get("sub"), "role": payload.get("role")}
        except Exception as e:
            logger.warning(f"Token decode error: {e}")

    logger.info(f"Auth: {request.method} {request.url.path} - User: {user['sub']} ({user['role']})")
    
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