import time
import jwt
import secrets

JWT_SECRET = secrets.token_urlsafe(32)
JWT_ALGORITHM = "HS256"


def token_response(token: str):
    return {
        "access token": token
    }


def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 6000
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str):
    try:
        real_token = token.split(" ")[1]
        decode_token = jwt.decode(real_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decode_token if decode_token["expiry"] >= time.time() else None
    except:
        return {}


def get_user_email(token: str):
    token = token.split(' ')[1]
    decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return decoded["userID"]