from flask import request, current_app, jsonify
import jwt
from functools import wraps
#from flask_jwt_extended import get_jwt_identity

class AuthError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message

def get_jwt_token():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise AuthError("Falta el header Authorization")

    parts = auth_header.split()

    if parts[0].lower() != 'bearer' or len(parts) != 2:
        raise AuthError("Formato inválido de Authorization header")
    
    return parts[1]

def verify_jwt_token():
    token = get_jwt_token()

    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
        print("✅Token verificado correctamente")
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError("Token expirado")
    except jwt.InvalidTokenError as e:
        raise AuthError(f"Token inválido: {str(e)}")
#def get_current_user_id():
#    return get_jwt_identity()

# src/utils/auth.py

def get_current_user_id():
    # Simula la extracción de un user_id desde un token
    payload = verify_jwt_token()
    user = payload.get('userId', {})
    return user

def jwt_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_token()
        except AuthError as e:
            print(f"❌Error de autenticación: {str(e)}")
            return jsonify({"error": str(e)}), 401
        return func(*args, **kwargs)
    return decorated