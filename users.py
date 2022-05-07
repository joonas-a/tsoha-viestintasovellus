import secrets
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT id, username, password FROM Users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_username"] = user.username
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["user_username"]
    del session["csrf_token"]

def register(username,password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO Users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)
