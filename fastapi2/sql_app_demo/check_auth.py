from jose import jwt  #type: ignore 

from .api.auth import SECRET_KEY, ALGORITHM


def token_verify_for_admin( token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    role: str = payload.get("role")
    if role == "admin":
        return True
    return False

def token_verify_for_student(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    role: str = payload.get("role")
    if role == "student":
        return True
    return False

def token_verify_for_teacher(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    role: str = payload.get("role")
    if role == "teacher":
        return True 
    return False
