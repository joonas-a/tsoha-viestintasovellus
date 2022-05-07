from email import message
from app import app
from db import db
from flask import render_template, request


@app.errorhandler(403)
def unauthorized_access(error):
    db.session.rollback()
    return render_template("error.html", title="403 Forbidden Access"), 403

@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", title="404 Not Found", \
        message="The file you were looking for is not here."), 404

@app.errorhandler(405)
def wrong_method(error):
    return render_template("error.html", title="405 Method Not Allowed", \
        message="Something went wrong"), 405

@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template("error.html", title="500 Internal Server Error"), 500
