from functools import wraps
from flask import Flask, request, jsonify, abort
# from firebase_admin import auth
from admin import apikey_ref
# A decorator to check auth
def apikey_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            apiKey = request.args.get("apiKey", None)
            apikey = request.args.get("apikey", None)
            keyFromDb = apikey_ref.document(apiKey or apikey).get()
            if (keyFromDb.exists):
                return f(*args, **kwargs)
            else:
                return abort(403, description="You are not authorized to access this resource")
        except:
            return abort(403, description="You are not authorized to access this resource")

    return decorated


