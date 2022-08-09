from django.conf import settings
from izzi.settings import SECRET_KEY
from .models import User
import jwt


def jwt_decode_handler(token):
    secret_key = SECRET_KEY
    print("settings : ",settings)
    return jwt.decode(
        token,
        secret_key,
        audinece = settings.SIMPLE_JWT.get("AUDIENCE"),
        issuer=settings.SIMPLE_JWT.get("ISSUER"),
        algorithms=[settings.SIMPLE_JWT.get("ALGORITHM")]
    )