from app import app
from flask import render_template, request, redirect, session
import boards, users


@app.route("/")
def index():
    list = boards.get_boards()
    return render_template("index.html", count=len(list), boards=list)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
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
    thread = boards.get_threads(id)
    name = boards.get_board_name(id)
    return render_template("board.html", board_name=name, board=id, threads=thread)

@app.route("/boards/<int:id>/new_thread")
def new_thread(id):
    return render_template("new_thread.html", board_id=id)

@app.route("/boards/<int:id>/create_new_thread", methods=["POST"])
def create_new_thread(id):
    title = request.form["title"]
    content = request.form["content"]
    board_id = request.form["board_id"]

    boards.new_thread(content, board_id, title)
    return redirect("/boards/" + str(board_id))