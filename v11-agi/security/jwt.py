import jwt

SECRET = "CHANGE_ME"


def verify(token):
    return jwt.decode(token, SECRET, algorithms=["HS256"])
