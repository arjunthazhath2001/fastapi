from jose import JWTError,jwt

SECRET_KWY="hello"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30


def create_access_token(data: dict):
    to_encode=data.copy()