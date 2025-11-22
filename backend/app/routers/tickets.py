from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import decode_access_token, decode_access_token_optional, require_role
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketOut

router = APIRouter()

# ---------- ADMIN CREATES A TICKET ----------
@router.post("/new", response_model=TicketOut, dependencies=[Depends(require_role("admin"))])
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    db_ticket = Ticket(**ticket.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

# ---------- LIST TICKETS ----------
@router.get("/", response_model=List[TicketOut])
def list_tickets(
    db: Session = Depends(get_db),
    payload: Optional[dict] = Depends(decode_access_token_optional)
):
    role = payload.get("role")
    user_id = payload.get("sub")

    if role == "user":
        return db.query(Ticket).filter(Ticket.user_id == user_id).all()

    # employee + admin see all tickets
    return db.query(Ticket).all()

# ---------- GET TICKET BY ID ----------
@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db), payload: dict = Depends(decode_access_token)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(404, "Ticket not found")

    role = payload.get("role")
    user_id = payload.get("sub")

    if role == "user" and ticket.user_id != user_id:
        raise HTTPException(403, "You cannot access another user's ticket")

    return ticket

# ---------- ADMIN UPDATES TICKET ----------
@router.put("/{ticket_id}", response_model=TicketOut, dependencies=[Depends(require_role("admin"))])
def update_ticket(ticket_id: int, ticket: TicketUpdate, db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(404, "Ticket not found")

    for key, value in ticket.dict(exclude_unset=True).items():
        setattr(db_ticket, key, value)

    db.commit()
    db.refresh(db_ticket)
    return db_ticket

# ---------- ADMIN DELETES TICKET ----------
@router.delete("/{ticket_id}", response_model=TicketOut, dependencies=[Depends(require_role("admin"))])
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(404, "Ticket not found")

    db.delete(db_ticket)
    db.commit()
    return db_ticket