from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

SECRET_KEY = 'supersecretkey'
ALGORITHM = 'HS256'

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email = payload.get('sub')
        role = payload.get('role')

        if email is None:
            raise HTTPException(status_code=401, detail='Invalid token')
        
        return {
            'email': email,
            'role': role
        }
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    