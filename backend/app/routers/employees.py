from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token_optional, require_role
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeOut
from typing import List, Optional
import logging
import traceback

logger = logging.getLogger(__name__)
router = APIRouter()

# Admin only create new employee
@router.post("/new", response_model=EmployeeOut, dependencies=[Depends(require_role("admin"))])
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = Employee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

# Get all employees - Version avec debug complet
@router.get("/", response_model=List[EmployeeOut])
def get_employees(db: Session = Depends(get_db), payload: Optional[dict] = Depends(decode_access_token_optional)):
    try:
        logger.info("=== DEBUG get_employees ===")
        logger.info(f"Payload received: {payload}")
        
        # Test de connexion DB
        logger.info("Testing database connection...")
        db_test = db.execute("SELECT 1").scalar()
        logger.info(f"DB test result: {db_test}")
        
        # Test de requête Employee
        logger.info("Querying Employee table...")
        employees = db.query(Employee).all()
        logger.info(f"Found {len(employees)} employees")
        
        for emp in employees:
            logger.info(f"Employee: {emp.id} - {emp.name}")
            
        return employees
        
    except Exception as e:
        logger.error(f"ERROR in get_employees: {e}")
        logger.error(f"Error type: {type(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Get employee by id - Version avec debug
@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db), payload: Optional[dict] = Depends(decode_access_token_optional)):
    try:
        logger.info(f"Getting employee {employee_id}")
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        logger.info(f"Found employee: {employee.name}")
        return employee
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_employee: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Admin only update employee by id
@router.put("/{employee_id}", response_model=EmployeeOut, dependencies=[Depends(require_role("admin"))])
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    for key, value in employee.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)

    db.commit()
    db.refresh(db_employee)
    return db_employee

# Admin only delete employee by id
@router.delete("/{employee_id}", response_model=EmployeeOut, dependencies=[Depends(require_role("admin"))])
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_employee)
    db.commit()
    return db_employee