from fastapi import HTTPException, status

InvalidTokenException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

ExpiredTokenException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")

EmailAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists"
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password"
)

YouDontHavePermissionException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission"
)
