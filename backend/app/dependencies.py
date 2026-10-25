from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.security import decode_access_token

bearer = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: Session = Depends(get_db)) -> User:
    unauthorized = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Valid bearer token required", headers={"WWW-Authenticate": "Bearer"})
    if not credentials:
        raise unauthorized
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise unauthorized
    try:
        user_id = int(payload["sub"])
    except (ValueError, TypeError):
        raise unauthorized
    user = db.get(User, user_id)
    if not user:
        raise unauthorized
    return user

def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user
