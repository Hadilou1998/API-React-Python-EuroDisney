from fastapi import FastAPI
from app.routers import users, attractions, tickets

app = FastAPI(
    title = "EuroDisney API",
    description = "API de gestion pour EuroDisney",
    version = "1.0.0"
)

# Inclure les routers
app.include_router(users.router, prefix="/auth", tags=["auth"])
app.include_router(attractions.router, prefix="/attractions", tags=["attractions"])
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])

@app.get("/")
async def root():
    return {"message": "Welcome to EuroDisney API"}