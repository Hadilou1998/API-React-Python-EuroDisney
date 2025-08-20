from fastapi import FastAPI
from app.routers import users, attractions, tickets, employees, reservations

app = FastAPI(
    title = "EuroDisney API",
    description = "API de gestion pour EuroDisney",
    version = "1.0.0"
)

# Inclure les routers
app.include_router(users.router, prefix="/auth", tags=["auth"])
app.include_router(attractions.router, prefix="/attractions", tags=["attractions"])
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(reservations.router, prefix="/reservations", tags=["reservations"])

@app.get("/")
async def root():
    return {"message": "Welcome to EuroDisney API"}