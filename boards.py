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
    sql = "SELECT DISTINCT T.id, T.title, T.created_at, U.username FROM Threads T, Boards B, Users U "\
        "WHERE T.b_id=:board_id AND T.u_id=U.id ORDER BY T.id DESC"
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
    sql = "SELECT T.title, T.content, T.created_at, U.username, T.id, T.u_id "\
        "FROM Threads T, Users U, Boards B "\
        "WHERE U.id=T.u_id AND T.id=:thread_id ORDER BY T.id"
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchone()

def edit_thread(thread_id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "UPDATE Threads SET content=:content "\
        "WHERE u_id=:user_id AND id=:thread_id"
    db.session.execute(sql, {"content":content, "user_id":user_id, "thread_id":thread_id})
    db.session.commit()
    return True

def get_comments(thread_id):
    sql = "SELECT  DISTINCT C.id, C.content, C.created_at, U.username, C.u_id FROM Comments C, Users U, Threads T "\
        "WHERE C.t_id=:thread_id AND C.u_id=U.id ORDER BY C.id DESC"
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchall()

def get_single_comment(comment_id):
    sql = "SELECT content FROM Comments WHERE id=:comment_id"
    result = db.session.execute(sql, {"comment_id":comment_id})
    return result.fetchone()[0]

def new_comment(content, thread_id):
    user_id = users.user_id()
    if user_id == 0 or len(content)<5:
        return False
    sql = "INSERT INTO Comments (t_id, u_id, created_at, content) "\
        "VALUES (:t_id, :u_id, NOW(), :content)"
    db.session.execute(sql, {"t_id":thread_id, "u_id":user_id, "content":content})
    db.session.commit()
    return True

def edit_comment(comment_id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "UPDATE Comments SET content=:content "\
        "WHERE u_id=:user_id AND id=:comment_id"
    db.session.execute(sql, {"content":content, "user_id":user_id, "comment_id":comment_id})
    db.session.commit()
    return True

def delete_comment(comment_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "DELETE FROM Comments "\
        "WHERE id=:comment_id AND u_id=:user_id"
    db.session.execute(sql, {"comment_id":comment_id, "user_id":user_id})
    db.session.commit()
    return True
