from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import decode_access_token, decode_access_token_optional, require_role
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate, ReservationOut

router = APIRouter()

# ---------- USER CREATES HIS RESERVATION ----------
@router.post("/new", response_model=ReservationOut, dependencies=[Depends(require_role("user"))])
def create_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(decode_access_token)
):
    user_id = payload.get("sub")
    new_reservation = Reservation(**reservation.dict(), user_id=user_id)
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation


# ---------- LIST RESERVATIONS ----------
@router.get("/", response_model=List[ReservationOut])
def list_reservations(
    db: Session = Depends(get_db),
    payload: Optional[dict] = Depends(decode_access_token_optional)
):
    if not payload:
        raise HTTPException(401, "Authentication required")

    role = payload.get("role")
    user_id = payload.get("sub")

    if role == "user":
        # user sees only his own reservations
        return db.query(Reservation).filter(Reservation.user_id == user_id).all()

    # employee + admin see all
    return db.query(Reservation).all()


# ---------- GET RESERVATION BY ID ----------
@router.get("/{reservation_id}", response_model=ReservationOut)
def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    payload: Optional[dict] = Depends(decode_access_token_optional)
):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(404, "Reservation not found")

    role = payload.get("role")
    user_id = payload.get("sub")

    if role == "user" and reservation.user_id != user_id:
        raise HTTPException(403, "You cannot access other users' reservations")

    return reservation


# ---------- UPDATE RESERVATION ----------
@router.put("/{reservation_id}", response_model=ReservationOut)
def update_reservation(
    reservation_id: int,
    reservation: ReservationUpdate,
    db: Session = Depends(get_db),
    payload: dict = Depends(decode_access_token)
):
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(404, "Reservation not found")

    role = payload.get("role")
    user_id = payload.get("sub")

    if role == "employee":
        raise HTTPException(403, "Employees cannot modify reservations")

    if role == "user" and db_reservation.user_id != user_id:
        raise HTTPException(403, "Cannot modify another user's reservation")

    # admin or owner can update
    for key, value in reservation.dict(exclude_unset=True).items():
        setattr(db_reservation, key, value)

    db.commit()
    db.refresh(db_reservation)
    return db_reservation


# ---------- DELETE RESERVATION ----------
@router.delete("/{reservation_id}", response_model=ReservationOut)
def delete_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(decode_access_token)
):
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(404, "Reservation not found")

    role = payload.get("role")
    user_id = payload.get("sub")

    if role == "employee":
        raise HTTPException(403, "Employees cannot delete reservations")

    if role == "user" and db_reservation.user_id != user_id:
        raise HTTPException(403, "Cannot delete another user's reservation")

    # admin or owner can delete
    db.delete(db_reservation)
    db.commit()
    return db_reservation