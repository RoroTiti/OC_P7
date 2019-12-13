from flask import Flask, request
from flask import render_template

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def render_question():
    data = request.form
    question = data["question"]
    return render_template("user_question.html", question=question)


@app.route("/answer", methods=["POST"])
def answer_question():
    pass
