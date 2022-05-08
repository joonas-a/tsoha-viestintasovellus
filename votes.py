from db import db
import users

def get_thread_votes(thread_id):
    sql = "SELECT SUM(vote) FROM Thread_Votes WHERE t_id=:thread_id"
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchone()[0]

def get_comment_votes(comment_id):
    sql = "SELECT SUM(vote) FROM Comment_Votes WHERE c_id=:comment_id"
    result = db.session.execute(sql, {"comment_id":comment_id})
    return result.fetchone()[0]

def has_voted_thread(thread_id):
    user_id = users.user_id()
    sql = "SELECT EXISTS(SELECT vote FROM Thread_Votes WHERE u_id=:user_id AND t_id=:thread_id)"
    result = db.session.execute(sql, {"user_id":user_id, "thread_id":thread_id})
    return result.fetchone()[0]

def has_voted_comment(comment_id):
    user_id = users.user_id()
    sql = "SELECT EXISTS(SELECT vote FROM Comment_Votes WHERE u_id=:user_id AND c_id=:comment_id)"
    result = db.session.execute(sql, {"user_id":user_id, "comment_id":comment_id})
    return result.fetchone()[0]

def vote_thread(thread_id, vote):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO Thread_Votes (vote, u_id, t_id) VALUES (:vote, :user_id, :thread_id)"
    db.session.execute(sql, {"vote":vote, "user_id":user_id, "thread_id":thread_id})
    db.session.commit()
    return True

def vote_comment(comment_id, vote):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO Comment_Votes (vote, u_id, c_id) VALUES (:vote, :user_id, :comment_id)"
    db.session.execute(sql, {"vote":vote, "user_id":user_id, "comment_id":comment_id})
    db.session.commit()
    return True

def get_thread_vote_status(thread_id): #only call this if the row exists, check using "has_voted_thread()"
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "SELECT vote FROM Thread_Votes WHERE u_id=:user_id AND t_id=:thread_id"
    result = db.session.execute(sql ,{"user_id":user_id, "thread_id":thread_id})
    return result.fetchone()[0]

def get_comment_vote_status(comment_id): #only call this if the row exists, check using "has_voted_thread()"
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "SELECT vote FROM Comment_Votes WHERE u_id=:user_id AND c_id=:comment_id"
    result = db.session.execute(sql ,{"user_id":user_id, "comment_id":comment_id})
    return result.fetchone()[0]

def change_vote_thread(thread_id, vote):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "UPDATE Thread_Votes SET vote=:vote WHERE u_id=:user_id AND t_id=:thread_id"
    db.session.execute(sql, {"vote":vote, "user_id":user_id, "thread_id":thread_id})
    db.session.commit()
    return True

def change_vote_comment(comment_id, vote):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "UPDATE Comment_Votes SET vote=:vote WHERE u_id=:user_id AND c_id=:comment_id"
    db.session.execute(sql, {"vote":vote, "user_id":user_id, "comment_id":comment_id})
    db.session.commit()
    return True
