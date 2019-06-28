from flask import Flask, jsonify
from flask.json import JSONEncoder
from MTGSpoilerBot import MTGSpoilerBot
from MTGCard import MTGCard
from MTGSet import MTGSet
from Database import Database
import psycopg2

app = Flask(__name__)


class MyJSONEncoder(JSONEncoder): #TODO: Auth
    def default(self, obj):
        if isinstance(obj, MTGCard):
            return {
                'Name': obj.name,
                'ReleaseDate': obj.release_date,
                'OracleTest': obj.oracle_text,
                'SetName': obj.set_name,
                'Url': obj.url,
                'Id': obj.id
            }
        if isinstance(obj, MTGSet):
            return {
                'Name': obj.name,
                'Code': obj.code,
                'ReleaseDate': obj.release_date,
                'CardCount': obj.card_count,
                'SetType': obj.set_type
            }
        return super(MyJSONEncoder, self).default(obj)


app.json_encoder = MyJSONEncoder


@app.route("/CheckForSets", methods=['GET'])
def check_for_sets():
    bot = MTGSpoilerBot()
    bot.check_for_new_sets()
    return jsonify(bot.current_sets)


@app.route("/CheckForCards/<mtg_set>", methods=['GET'])
def check_for_cards(mtg_set):
    bot = MTGSpoilerBot()
    bot.check_for_new_sets()
    cards = bot.check_for_new_cards()
    return jsonify(cards)


@app.route("/test")
def test():
    bot = MTGSpoilerBot()
    bot.get_all_sets()
    db = Database()
    #db.insert_sets([bot.current_sets[0]])
    return jsonify(db.get_sets())

# @app.route("/ConfigureTables")
# def configure_tables():
#         db = DatabaseInstaller()
#         db.setup_tables()
#         return 'nice'
