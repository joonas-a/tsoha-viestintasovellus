from app import app
from flask import render_template, request, redirect, session
import boards


@app.route("/")
def index():
    list = boards.get_boards()
    return render_template("index.html", count=len(list), boards=list)
