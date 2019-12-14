import random
import string

import requests
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

    search_term = parse_question(question)

    if search_term == "":
        html = render_template("grand_py_error_answer.html",
                               error="Ta question semble incomplète ou mal formulée, je ne la comprends pas bien... Peux tu réessayer ?")
    else:
        try:
            factory = OpenStreetMapBotFactory(search_term)
            osm: OpenStreetMapBot = factory.get_object()

            html = render_template("grand_py_osm_answer.html",
                                   osm=osm,
                                   uuid=uuid_generator())

            factory = OpenMediaWikiBotFactory(osm.latitude, osm.longitude)
            omw: OpenMediaWikiBot = factory.get_object()

            html += render_template("grand_py_omw_answer.html",
                                    omw=omw)
        except IndexError:
            html = render_template("grand_py_error_answer.html",
                                   error="Je n'ai rien trouvé pour répondre à ta question... Peut-être comporte-t-elle une erreur ?")

        except requests.exceptions.ConnectionError:
            html = render_template("grand_py_error_answer.html",
                                   error="Mince, je n'ai pas réussi à consulter mes archives... Elles sont momentanément indisponibles.")

    return html


def uuid_generator(string_length=30) -> str:
    """Generate a random string of letters and digits """
    letters_and_digits = string.ascii_letters + string.digits
    return "map_" + ''.join(random.choice(letters_and_digits) for i in range(string_length))


def parse_question(question) -> str:
    determinants = ["le", "la", "l", "les", "de", "du", "d"]
    verbs = ["situe", "situent", "adresse"]

    if not any(word in question for word in verbs) or not "?" in question:
        return ""

    question = question.replace("'", " ")
    words_list = question.split(" ")

    verb_index = 0
    for verb in verbs:
        if verb in words_list:
            verb_index = words_list.index(verb)
            break

    try:
        if words_list[verb_index + 1] in determinants:
            words_list.pop(verb_index + 1)
    except IndexError:
        return ""

    question = " ".join(words_list)
    words_list = question.split(" ")

    search_term, start_index, end_index = "", 0, 0

    try:
        for verb in verbs:
            if verb in question:
                for i in range(0, len(words_list)):
                    if verb in words_list[i]:
                        start_index = i + 1
                    elif words_list[i] == "?":
                        end_index = i
                        break
    except IndexError:
        return ""

    for i in range(start_index, end_index):
        search_term += words_list[i] + " "

    return search_term.rstrip()
