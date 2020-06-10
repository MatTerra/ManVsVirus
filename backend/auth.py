import os
from jose import jwt, JWTError
from flask import abort

JWT_SECRET = os.environ.get('JWT_SECRET')


def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except JWTError as e:
        return abort(401, "Unauthorized")
