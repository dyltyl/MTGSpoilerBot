from flask import Flask
from MTGSpoilerBot import MTGSpoilerBot
app = Flask(__name__)


@app.route("/CheckForSets", methods=['GET'])
def check_for_sets():
    bot = MTGSpoilerBot()
    bot.check_for_new_sets()
    return bot.current_sets


@app.route("/CheckForCards/<mtg_set>", methods=['GET'])
def check_for_cards(mtg_set):
    bot = MTGSpoilerBot()
    bot.check_for_new_cards()
    return bot.current_cards

