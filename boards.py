from db import db
import users

def get_boards():
    sql = "SELECT B.id, B.title FROM Boards B"
    result = db.session.execute(sql)
    return result.fetchall()

def get_board_name(board_id):
    sql = "SELECT B.title FROM Boards B WHERE B.id=:board_id"
    result = db.session.execute(sql, {"board_id":board_id})
    return result.fetchone()[0]

def get_all_threads(board_id):
    sql = "SELECT DISTINCT T.id, T.title, T.created_at FROM Threads T, Boards B "\
        "WHERE T.b_id=:board_id ORDER BY T.id DESC"
    result = db.session.execute(sql, {"board_id":board_id})
    return result.fetchall()

def new_thread(content, board_id, title):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO Threads (content, u_id, b_id, created_at, title) "\
        "VALUES (:content, :u_id, :b_id, NOW(), :title)"
    db.session.execute(sql, {"content":content, "u_id":user_id, "b_id":int(board_id), "title":title})
    db.session.commit()
    return True

def get_single_thread(thread_id):
    sql = "SELECT T.title, T.content, T.created_at, U.username, T.id "\
        "FROM Threads T, Users U, Boards B "\
        "WHERE U.id=T.u_id AND T.id=:thread_id ORDER BY T.id"
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchone()