from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Header

# Config JWT
SECRET_KEY = "mykey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ------------------------------
# Password utils
# ------------------------------
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# ------------------------------
# JWT creation
# ------------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ------------------------------
# STRICT token decode (always required)
# ------------------------------
def decode_access_token(authorization: str = Header(None)) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    # Accept "Authorization" or "authorization"
    auth = authorization.lower()
    if not auth.startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split(" ")[1]

    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ------------------------------
# OPTIONAL token decode (returns None)
# ------------------------------
def decode_access_token_optional(authorization: Optional[str] = Header(None)) -> Optional[dict]:
    if not authorization:
        return None

    parts = authorization.split()

    # Must be exactly: Bearer <token>
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    token = parts[1]  # clean token ONLY

    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

# ------------------------------
# Role checker
# ------------------------------
def require_role(role: str):
    def role_checker(payload: dict = Depends(decode_access_token)):
        if payload.get("role") != role:
            raise HTTPException(status_code=403, detail="Access denied")
        return payload
    return role_checker