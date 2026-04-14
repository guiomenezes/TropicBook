from fastapi import Depends, HTTPException
from app. auth.deps import get_current_user

def require_role(allowed_roles: list):
    def role_ckecker(user = Depends(get_current_user)):
        if user['role'] not in allowed_roles:
            raise HTTPException(status_code=403, detail='Permission denied.')
        return user
    return role_ckecker