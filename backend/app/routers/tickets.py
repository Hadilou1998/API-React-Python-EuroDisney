from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token, require_role
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketOut
from typing import List

router = APIRouter()

# Create a new ticket for the user
@router.post("/", response_model=TicketOut)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db), payload: dict = Depends(decode_access_token)):
    user_id = payload.get("user_id")
    db_ticket = Ticket(**ticket.dict(), user_id=user_id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

# List all tickets for the user
@router.get("/", response_model=List[TicketOut])
def get_tickets(db: Session = Depends(get_db), payload: dict = Depends(decode_access_token)):
    user_id = payload.get("user_id")
    return db.query(Ticket).filter(Ticket.user_id == payload.get("user_id")).all()

# Get a specific ticket for the user
@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

# Admin only can update a ticket for the user
@router.put("/{ticket_id}", response_model=TicketOut)
def update_ticket(ticket_id: int, ticket: TicketUpdate, db: Session = Depends(get_db), payload: dict = Depends(require_role("admin"))):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    for key, value in ticket.dict(exclude_unset=True).items():
        setattr(db_ticket, key, value)
    db.commit()
    db.refresh(db_ticket)
    return {"message": "Ticket updated successfully"}

# Admin only can delete a ticket for the user
@router.delete("/{ticket_id}", response_model=TicketOut)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db), payload: dict = Depends(require_role("admin"))):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db.delete(db_ticket)
    db.commit()
    return {"message": "Ticket deleted successfully"}