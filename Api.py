from flask import Flask
app = Flask(__name__)


@app.route("/CheckForSets", methods=['GET'])
def check_for_sets():
    return "Hello World!"


@app.route("/CheckForCards/<mtg_set>", methods=['GET'])
def check_for_cards(mtg_set):
    return mtg_set

