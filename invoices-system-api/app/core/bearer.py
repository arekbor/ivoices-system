from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.api.endpoints.user import functions as user_functions

class JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail="Invalid token or expired token."
                )
            return credentials.credentials
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid authorization code."
        )
    
    def verify_jwt(self, jwt_token: str) -> bool:
        is_token_valid = False
        try:
            payload = user_functions.decode_jwt(jwt_token)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid