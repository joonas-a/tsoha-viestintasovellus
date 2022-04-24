from db import db

def get_boards():
    sql = "SELECT B.title FROM Boards B"
    result = db.session.execute(sql)
    return result.fetchall()

def get_threads():
    sql = "SELECT T.id, T.content, T.created_at FROM Threads T, Boards B WHERE T.b_id = B.id"
    result = db.session.execute(sql)
    return result.fetchall()