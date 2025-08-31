from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import decode_access_token, require_role
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate, ReservationOut

router = APIRouter()

# Create a new reservation
@router.post("/", response_model=ReservationOut)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db), payload: dict = Depends(decode_access_token)):
    user_id = payload.get("user_id")
    new_reservation = Reservation(**reservation.dict(), user_id=user_id)
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation

# Get all reservations
@router.get("/", response_model=List[ReservationOut])
def list_reservations(db: Session = Depends(get_db), payload: dict = Depends(decode_access_token)):
    user_id = payload.get("user_id")
    return db.query(Reservation).filter(Reservation.user_id == user_id).all()

# Get a reservation by id
@router.get("/{reservation_id}", response_model=ReservationOut)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

# Admin only update a reservation
@router.put("/{reservation_id}", response_model=ReservationOut, dependencies=[Depends(require_role("admin"))])
def update_reservation(reservation_id: int, reservation: ReservationUpdate, db: Session = Depends(get_db)):
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    for key, value in reservation.dict(exclude_unset=True).items():
        setattr(db_reservation, key, value)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

# Admin only delete a reservation
@router.delete("/{reservation_id}", response_model=ReservationOut, dependencies=[Depends(require_role("admin"))])
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    db.delete(db_reservation)
    db.commit()
    return db_reservation