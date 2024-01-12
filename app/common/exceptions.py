from fastapi import HTTPException, status

InvalidTokenException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

ExpiredTokenException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")
