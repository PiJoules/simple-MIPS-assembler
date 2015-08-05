"""`main` is the top level module for your Flask application."""

from mips_parser import *

# Import the Flask Framework
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
	return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate_mips():
	code = request.form.getlist("code[]")
	if code != []:
		return jsonify(result=translate(code))
	else:
		return jsonify(result=[1,"Did not receive 'code' parameter"])


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
