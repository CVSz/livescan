import jwt

SECRET = "CHANGE_ME"


def verify(token: str):
    return jwt.decode(token, SECRET, algorithms=["HS256"])
