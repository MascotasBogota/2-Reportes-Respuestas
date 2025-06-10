from flask import request
from flask_jwt_extended import get_jwt_identity

#def get_current_user_id():
#    return get_jwt_identity()

# src/utils/auth.py

def get_current_user_id():
    # Simula la extracción de un user_id desde un token
    return "user_dev_123"

