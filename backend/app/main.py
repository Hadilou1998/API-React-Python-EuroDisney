from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
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

# Middleware perso pour forcer les en-tetes CORS
@app.middleware("http")
async def cors_handler(request: Request, call_next):
    # Log la requête
    logger.info(f"Request: {request.method} {request.url}")
    origin = request.headers.get("origin")
    logger.info(f"Origin: {origin}")
    
    # Gestion spéciale pour OPTIONS (preflight)
    if request.method == "OPTIONS":
        response = Response()
        
        # Vérifier que l'origin est autorisée
        if origin in origins:
            response.headers["Access-Control-Allow-Origin"] = origin
        else:
            response.headers["Access-Control-Allow-Origin"] = origins[0]  # Fallback
            
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Max-Age"] = "86400"  # Cache preflight 24h
        
        return response
    
    # Traiter la requête normale
    response = await call_next(request)
    
    # Ajouter les en-têtes CORS à la réponse
    if origin in origins:
        response.headers["Access-Control-Allow-Origin"] = origin
    else:
        response.headers["Access-Control-Allow-Origin"] = origins[0]  # Fallback
        
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    
    logger.info(f"Response status: {response.status_code}")
    
    return response

# Middleware pour logs et JWT
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Skip pour OPTIONS déjà géré
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

    logger.info(f"Auth Request: {request.method} {request.url.path} - User: {user['sub']} - Role: {user['role']}")
    
    response = await call_next(request)
    
    logger.info(f"Auth Response: {request.method} {request.url.path} - Status: {response.status_code}")
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