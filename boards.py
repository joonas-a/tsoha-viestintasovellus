from db import db

def get_boards():
    sql = "SELECT B.title FROM Boards B"
    result = db.session.execute(sql)
    return result.fetchall()