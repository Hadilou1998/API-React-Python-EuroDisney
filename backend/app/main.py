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

# En-têtes explicitement autorisés
allowed_headers = [
    "accept",
    "accept-encoding",
    "authorization",  # CRUCIAL
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # IMPORTANT pour avec credentials
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=allowed_headers,
    expose_headers=["*"],
)

# Middleware OPTIONS preflight personnalisé
@app.middleware("http")
async def cors_preflight_middleware(request: Request, call_next):
    # Gestion spéciale et complète des requêtes OPTIONS
    if request.method == "OPTIONS":
        origin = request.headers.get("origin", "")
        
        # Créer une réponse OPTIONS avec tous les en-têtes nécessaires
        response = Response(status_code=200)
        
        # Origin
        if origin in origins:
            response.headers["Access-Control-Allow-Origin"] = origin
        else:
            response.headers["Access-Control-Allow-Origin"] = origins[0]
        
        # Credentials
        response.headers["Access-Control-Allow-Credentials"] = "true"
        
        # Methods
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        
        # Headers - EXPLICITLY include authorization
        requested_headers = request.headers.get("access-control-request-headers", "")
        if requested_headers:
            # Valider que les en-têtes demandés sont autorisés
            headers_list = [h.strip().lower() for h in requested_headers.split(",")]
            valid_headers = [h for h in headers_list if h in [ah.lower() for ah in allowed_headers]]
            response.headers["Access-Control-Allow-Headers"] = ", ".join(valid_headers)
        else:
            # Par défaut, autoriser tous nos en-têtes autorisés
            response.headers["Access-Control-Allow-Headers"] = ", ".join(allowed_headers)
        
        # Cache preflight
        response.headers["Access-Control-Max-Age"] = "86400"
        
        logger.info(f"OPTIONS preflight: {dict(response.headers)}")
        return response
    
    # Pour les requêtes normales
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Request failed: {e}")
        response = Response(status_code=500, content="Internal server error")
    
    # Ajouter les en-têtes CORS aux réponses normales
    origin = request.headers.get("origin", "")
    if origin in origins:
        response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Credentials"] = "true"
    
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