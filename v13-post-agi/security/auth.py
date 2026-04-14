import jwt

SECRET = "CHANGE_ME"


def verify(t):
    return jwt.decode(t, SECRET, algorithms=["HS256"])
