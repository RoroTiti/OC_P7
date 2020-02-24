import random
import string

import spacy
from flask import Flask, request
from flask import render_template

from grandpybot.chatbots.chatbotfactory import OpenStreetMapBotFactory, OpenMediaWikiBotFactory
from grandpybot.chatbots.openmediawiki import OpenMediaWikiBot
from grandpybot.chatbots.openstreetmap import OpenStreetMapBot

app = Flask(__name__)

print("Loading spaCy...")
nlp = spacy.load("fr_core_news_md")
print("spaCy loaded!")


@app.route("/", methods=["GET"])
def index():
    """
    Main app route, showing the chat page
    """
    return render_template("index.html")


@app.route("/", methods=["POST"])
def render_question():
    """
    Returns the HTML corresponding to a user answer asked to a chat bot
    """
    data = request.form
    question = data["question"]
    return render_template("user_question.html", question=question)


@app.route("/answer", methods=["POST"])
def answer_question():
    """
    Return the HTML corresponding to an answer from a chat bot
    """
    data = request.form
    question = data["question"]

    search_term = parse_question(question)

    if search_term == "":
        html = render_template("grand_py_error_answer.html",
                               error="Ta question semble incomplète ou mal formulée, je ne la comprends pas bien... Peux-tu réessayer ?")
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

    return html


def uuid_generator(string_length=30) -> str:
    """
    Generate a random string of letters and digits, used to generate a random LeafLet map HTML ID attribute
    """
    letters_and_digits = string.ascii_letters + string.digits
    return "map_" + ''.join(random.choice(letters_and_digits) for i in range(string_length))


def parse_question(question) -> str:
    """
    User question parser returning the search term from a user question
    """
    doc = nlp(question)

    keywords = []
    words_to_check = []

    for token in doc:
        if token.pos_ == "VERB":
            for child in token.children:
                if child.pos_ in ["NOUN", "PROPN", "ADJ"]:
                    keywords.append(child)
                    words_to_check.append(child)

    while len(words_to_check) > 0:
        for child in words_to_check[0].children:
            if child.pos_ in ["NOUN", "PROPN", "ADJ"]:
                keywords.append(child)
                words_to_check.append(child)

        words_to_check.pop(0)

    keywords.sort(key=lambda x: x.idx)

    for keyword in keywords:
        if keyword.lemma_ in ["adresse"]:
            keywords.remove(keyword)

    if len(keywords) > 0:
        idx_start = keywords[0].idx
        idx_end = keywords[len(keywords) - 1].idx + len(keywords[len(keywords) - 1].text)

        assembled_keywords = "".join(list(question)[idx_start:idx_end])

        return assembled_keywords

    else:
        return ""
