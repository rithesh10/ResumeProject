from functools import wraps
import jwt
from flask import request,g
from app.utils.ApiError import ApiError  # Custom ApiError class
from db.db import mongo
import os
from bson import ObjectId
SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET")  # You can store this in config

def verify_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('accessToken') or request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token.replace('Bearer ', '')

        if not token:
            raise ApiError(401, "Unauthorized request")

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # Attach the user data to the request object
            # print(decoded_token)

            user=mongo.db.users.find_one({"_id":ObjectId(decoded_token.get("user_id"))})
            # print(user)
            if not user:
                 raise ApiError(404, "User not found")

            # Convert ObjectId to string and store in g
            g.user = user  # Store full user object
            g.user["_id"] = str(user["_id"])  # Convert _id to string
            # print(user)
            # print(g.user["_id"])
            
        except jwt.ExpiredSignatureError:
            raise ApiError(401, "Token has expired")
        except jwt.InvalidTokenError:
            raise ApiError(401, "Token is invalid")

        return f(*args, **kwargs)

    return decorated_function
