from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.attraction import Attraction, AttractionStatus
from app.schemas.attraction import AttractionCreate, AttractionUpdate, AttractionOut
from typing import List

router = APIRouter()

@router.post("/", response_model=AttractionOut)
def create_attraction(attraction: AttractionCreate, db: Session = Depends(get_db)):
    new_attraction = Attraction(**attraction.dict())
    db.add(new_attraction)
    db.commit()
    db.refresh(new_attraction)
    return new_attraction

@router.get("/", response_model=List[AttractionOut])
def read_attractions(db: Session = Depends(get_db)):
    attractions = db.query(Attraction).all()
    return attractions

@router.get("/{attraction_id}", response_model=AttractionOut)
def read_attraction(attraction_id: int, db: Session = Depends(get_db)):
    attraction = db.query(Attraction).filter(Attraction.id == attraction_id).first()
    if not attraction:
        raise HTTPException(status_code=404, detail="Attraction not found")
    return attraction

@router.put("/{attraction_id}", response_model=AttractionOut)
def update_attraction(attraction_id: int, attraction: AttractionUpdate, db: Session = Depends(get_db)):
    db_attraction = db.query(Attraction).filter(Attraction.id == attraction_id).first()
    if not db_attraction:
        raise HTTPException(status_code=404, detail="Attraction not found")
    for key, value in attraction.dict(exclude_unset=True).items():
        setattr(db_attraction, key, value)
    db.commit()
    db.refresh(db_attraction)
    return {"message": "Attraction updated successfully"}

@router.delete("/{attraction_id}", response_model=AttractionOut)
def delete_attraction(attraction_id: int, db: Session = Depends(get_db)):
    db_attraction = db.query(Attraction).filter(Attraction.id == attraction_id).first()
    if not db_attraction:
        raise HTTPException(status_code=404, detail="Attraction not found")
    db.delete(db_attraction)
    db.commit()
    return {"message": "Attraction deleted successfully"}