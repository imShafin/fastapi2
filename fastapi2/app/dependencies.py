from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .auth import verify_token
from .schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    user = verify_token(token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

def admin_required(current_user: TokenData = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")

def teacher_required(current_user: TokenData = Depends(get_current_user)):
    if current_user.role not in ['admin', 'teacher']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Teacher privileges required")