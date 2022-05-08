from app import app
from flask import render_template, request, redirect, session, abort
import boards, users, votes


@app.route("/")
def index():
    list = boards.get_boards()
    return render_template("index.html", count=len(list), boards=list)

@app.route("/logout")
def logout():
    users.logout()
    return redirect(request.referrer)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return redirect("/")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            if request.referrer == "/login":
                return redirect("/")
            return redirect(request.referrer)
        else:
            return render_template("error.html", message="Username or password is wrong")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if len(username) < 4 or len(username) > 16:
            return render_template("error.html", message="Username too short or long")
        if len(password1) < 6:
            return render_template("error.html", message="Password too short")
        if len(password1) > 50:
            return render_template("error.html", message="Password too long (keep it under 50 chars)")
        if password1 != password2:
            return render_template("error.html", message="The passwords did not match")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Registration failed (username may be taken)")

@app.route("/boards/<int:id>")
def board(id):
    thread = boards.get_all_threads(id)
    name = boards.get_board_name(id)
    return render_template("board.html", board_name=name, board_id=id, threads=thread, count=len(thread))

@app.route("/boards/<int:id>/new_thread", methods=["GET", "POST"])
def new_thread(id):
    if request.method == "GET":
        board_name = boards.get_board_name(id)
        return render_template("new_thread.html", board_id=id, board_name=board_name)

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        title = request.form["title"]
        if len(title) < 5 or len(title) > 40:
            return render_template("error.html", message="Title needs to be 5-40 characters long.")
        content = request.form["content"]
        if len(content) > 1000:
            return render_template("error.html", message="Message needs to be under 1000 characters.")
        board_id = request.form["board_id"]
        boards.new_thread(content, board_id, title)
        return redirect("/boards/" + str(board_id))

@app.route("/boards/<int:id>/<int:thread_id>/edit_thread", methods=["GET", "POST"])
def edit_thread(id, thread_id):
    if request.method == "GET":
        thread = boards.get_single_thread(thread_id)
        return render_template("edit_thread.html", title=thread[0], content=thread[1], \
            board_id=id, thread_id=thread_id)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        edited_message = request.form["message"]
        if len(edited_message) > 1000:
            return render_template("error.html", message="Message needs to be under 1000 characters.")
        boards.edit_thread(thread_id, edited_message)
        return redirect("/boards/" + str(id) + "/" + str(thread_id))

@app.route("/boards/<int:id>/<int:thread_id>/delete_thread", methods=["POST"])
def delete_thread(id, thread_id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    boards.delete_thread(thread_id)
    return redirect("/boards/" + str(id))

@app.route("/boards/<int:id>/<int:thread_id>")
def thread(id, thread_id):
    thread = boards.get_single_thread(thread_id)
    board_name = boards.get_board_name(id)
    comments = boards.get_comments(thread_id)
    thread_votes = votes.get_thread_votes(thread_id)
    comment_votes = {}
    for comment in comments:
        comment_votes[comment[0]]=votes.get_comment_votes(comment[0])
    return render_template("thread.html", title=thread[0], content=thread[1], timestamp=thread[2], \
        creator=thread[3], comments=comments, thread_id=thread_id, board_id=id, board_name=board_name, \
            creator_id=thread[5], thread_votes=thread_votes, comment_votes=comment_votes)

@app.route("/boards/<int:id>/<int:thread_id>/new_comment", methods=["POST"])
def new_comment(id, thread_id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    message = request.form["message"]
    if len(message) > 1000 or len(message) < 5:
        return render_template("error.html", message="Message needs to be between 5-1000 characters.")
    boards.new_comment(message, thread_id)
    return redirect("/boards/" + str(id) + "/" + str(thread_id))

@app.route("/boards/<int:id>/<int:thread_id>/edit_comment/<int:comment_id>", methods=["GET", "POST"])
def edit_comment(id, thread_id, comment_id):
    if request.method == "GET":
        old_comment = boards.get_single_comment(comment_id)
        return render_template("edit_comment.html", board_id=id, thread_id=thread_id, comment_id=comment_id, \
            old_comment=old_comment)

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        new_message = request.form["message"]
        if len(new_message) > 1000 or len(new_message) < 5:
            return render_template("error.html", message="Message needs to be between 5-1000 characters.")
        boards.edit_comment(comment_id, new_message)
        return redirect("/boards/" + str(id) + "/" + str(thread_id))

@app.route("/boards/<int:id>/<int:thread_id>/delete_comment/<int:comment_id>")
def delete_comment(id, thread_id, comment_id):
    boards.delete_comment(comment_id)
    return redirect(request.referrer)

@app.route("/boards/<int:id>/<int:thread_id>/vote", methods=["POST"])
def vote_thread(id, thread_id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    has_voted = votes.has_voted_thread(thread_id)
    if has_voted == False:
        if request.form["action"] == "Upvote":
            votes.vote_thread(thread_id, 1)
        elif request.form["action"] == "Downvote":
            votes.vote_thread(thread_id, -1)
    else:
        current_vote = votes.get_thread_vote_status(thread_id)
        if current_vote == 1 and request.form["action"] == "Upvote":
            votes.change_vote_thread(thread_id, 0)
        elif current_vote == 0 and request.form["action"] == "Upvote":
            votes.change_vote_thread(thread_id, 1)
        elif current_vote == -1 and request.form["action"] == "Downvote":
            votes.change_vote_thread(thread_id, 0)
        elif current_vote == -0 and request.form["action"] == "Downvote":
            votes.change_vote_thread(thread_id, -1)
        elif current_vote == -1 and request.form["action"] == "Upvote":
            votes.change_vote_thread(thread_id, 1)
        elif current_vote == 1 and request.form["action"] == "Downvote":
            votes.change_vote_thread(thread_id, -1)
    return redirect("/boards/" + str(id) + "/" + str(thread_id))

@app.route("/boards/<int:id>/<int:thread_id>/<int:comment_id>/vote", methods=["POST"])
def vote_comment(id, thread_id, comment_id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    has_voted = votes.has_voted_comment(comment_id)
    if has_voted == False:
        if request.form["action"] == "Upvote":
            votes.vote_comment(comment_id, 1)
        elif request.form["action"] == "Downvote":
            votes.vote_comment(comment_id, -1)
    else:
        current_vote = votes.get_comment_vote_status(comment_id)
        if current_vote == 1 and request.form["action"] == "Upvote":
            votes.change_vote_comment(comment_id, 0)
        elif current_vote == 0 and request.form["action"] == "Upvote":
            votes.change_vote_comment(comment_id, 1)
        elif current_vote == -1 and request.form["action"] == "Downvote":
            votes.change_vote_comment(comment_id, 0)
        elif current_vote == -0 and request.form["action"] == "Downvote":
            votes.change_vote_comment(comment_id, -1)
        elif current_vote == -1 and request.form["action"] == "Upvote":
            votes.change_vote_comment(comment_id, 1)
        elif current_vote == 1 and request.form["action"] == "Downvote":
            votes.change_vote_comment(comment_id, -1)
    return redirect("/boards/" + str(id) + "/" + str(thread_id))
