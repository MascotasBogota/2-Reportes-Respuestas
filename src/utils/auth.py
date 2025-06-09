from flask import request

def get_current_user_id():
    return request.headers.get("X-User-Id", "user_demo")
