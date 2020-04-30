from functools import wraps
from flask import Flask, request, jsonify, abort
from firebase_admin import auth
# A decorator to check auth
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        decoded_token = get_user()
        if (decoded_token):
            return f(*args, **kwargs)
        else:
            return abort(403, description="You are not authorized to access this resource")
    return decorated

# a function to get logged in user
def get_user():
    try:
        id_token = request.headers['Authorization'].split(' ').pop()
        decoded_token = auth.verify_id_token(id_token)
        # uid = decoded_token['uid']
        return decoded_token
    except:
        abort(403, description="You are not authorized to access this resource")


# a function to get logged in user id
def get_user_id():
    try:
        id_token = request.headers['Authorization'].split(' ').pop()
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return uid
    except:
        abort(403, description="You are not authorized to access this resource")

