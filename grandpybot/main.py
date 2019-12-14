import random
import string

from flask import Flask, request
from flask import render_template

from grandpybot.chatbots.chatbotfactory import OpenStreetMapBotFactory, OpenMediaWikiBotFactory
from grandpybot.chatbots.openmediawiki import OpenMediaWikiBot
from grandpybot.chatbots.openstreetmap import OpenStreetMapBot

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
    data = request.form
    question = data["question"]

    factory = OpenStreetMapBotFactory(question)
    osm: OpenStreetMapBot = factory.get_object()

    html = render_template("grand_py_osm_answer.html",
                           latitude=osm.latitude,
                           longitude=osm.longitude,
                           uuid=uuid_generator())

    factory = OpenMediaWikiBotFactory(osm.latitude, osm.longitude)
    omw: OpenMediaWikiBot = factory.get_object()

    return html


def uuid_generator(string_length=30) -> str:
    """Generate a random string of letters and digits """
    letters_and_digits = string.ascii_letters + string.digits
    return "map_" + ''.join(random.choice(letters_and_digits) for i in range(string_length))
