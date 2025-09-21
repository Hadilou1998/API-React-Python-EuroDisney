from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token_optional, require_role
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeOut
from typing import List, Optional

router = APIRouter()

# Admin only create new employee
@router.post("/new", response_model=EmployeeOut, dependencies=[Depends(require_role("admin"))])
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = Employee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

# Get all employees
@router.get("/", response_model=List[EmployeeOut])
def get_employees(db: Session = Depends(get_db), payload: Optional[dict] = Depends(decode_access_token_optional)):
    # Access control
    if not payload:
        return []
    
    role = payload.get("role")
    user_id = payload.get("sub")

    if role == "admin":
        # admin can see all employees
        return db.query(Employee).all()
    
    if role == "employee":
        # employee can see all employees
        return db.query(Employee).all()
    
    raise HTTPException(status_code=403, detail="Access denied")

# Get employee by id
@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db), payload: Optional[dict] = Depends(decode_access_token_optional)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # if not payload, we can return employee without access control
    if not payload:
        return employee
    
    # Access control
    role = payload.get("role")
    user_id = payload.get("sub")

    if role == "admin":
        # admin can see all employees
        return employee
    elif role == "employee" and str(user_id) == str(employee_id):
        # employee can see his own information
        return employee
    elif role == "employee":
        return employee
    else:
        raise HTTPException(status_code=403, detail="Access denied")

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