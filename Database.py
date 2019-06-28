import psycopg2
import os
from MTGSet import MTGSet
from MTGCard import MTGCard
from typing import List


class DatabaseInstaller:
    def __init__(self):
        print('Connecting to db')
        parts = os.environ['DATABASE_URL'].split(":")
        print(os.environ['DATABASE_URL'])
        self.username = parts[1][2:]
        self.password = parts[2][0:parts[2].index("@")]
        self.host = parts[2][parts[2].index('@')+1:]
        self.port = parts[3][0:parts[3].index('/')]
        self.database = parts[3][parts[3].index("/") + 1:]
        self.path = os.path.realpath(__file__)
        try:
            self.path = self.path[0:self.path.rindex('/')]
        except ValueError:
            self.path = self.path[0:self.path.rindex('\\')]
        print('username: ' + self.username)
        print('password: ' + self.password)
        print('database: ' + self.database)
        print('host: ' + self.host)
        print('port: ' + self.port)
        print('path: ' + self.path)
        print(type(self.connect_to_database()))

    def connect_to_database(self): #Todo: add null checks/etc
        return psycopg2.connect("dbname="+self.database+" user="+self.username+" password="+self.password + " host="+self.host + " port="+self.port)

    def check_table_exists(self, table: str) -> bool:
        database = self.connect_to_database()
        cursor = database.cursor()
        cursor.execute("SELECT 1 FROM information_schema.tables WHERE table_name = '"+table+"';")
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return False
        return True

    def create_table(self, tablename: str, filename: str):
        if not self.check_table_exists(tablename):
            database = self.connect_to_database()
            sql_file = open(filename, "r")
            sql = sql_file.read()
            sql_file.close()
            cursor = database.cursor()
            cursor.execute(sql)
            database.commit()
            cursor.close()
            sql_file.close()
        else:
            print(tablename + ' needs updating')

    def setup_tables(self):
        self.create_table('mtg_set', self.path+'/MTG_Set.sql')
        print('Created MTG_Set', self.check_table_exists('mtg_set'))
        self.create_table('cards', self.path + '/Cards.sql')

    def get_cards_from_set(self, mtg_set: str):
        database = self.connect_to_database()
        cursor = database.cursor()
        cursor.execute('SELECT * FROM cards WHERE mtg_set = ' + mtg_set)
        result = cursor.fetchone()
        cursor.close()

    def insert_cards(self, cards: List[MTGCard]):
        if len(cards) < 1:
            return
        database = self.connect_to_database()
        format_string = '({}, {}, {}, {}, {}, {})'
        sql = 'INSERT INTO cards (name, release_date, oracle_text, url, mtg_set, id) VALUES '
        values = []
        for card in cards:
            values.append(format_string.format(card.name, card.release_date, card.oracle_text, card.url, card.set_name, card.id))
        sql += ', '.join(values) + ';'
        print(sql)
        cursor = database.cursor()
        cursor.execute(sql)
        database.commit()
        cursor.close()

    def update_cards(self, cards: List[MTGCard]):
        if len(cards) < 1:
            return
        database = self.connect_to_database()
        format_string = '({}, {}, {}, {}, {}, {})'
        sql = 'UPDATE cards as c SET ' \
              'name = c2.name, ' \
              'release_date = c2.release_date,' \
              ' oracle_text = c2.oracle_text, ' \
              'url = c2.url, ' \
              'set_name = c2.set_name, ' \
              'id = c2.id FROM (VALUES'
        values = []
        for card in cards:
            values.append(format_string.format(card.name, card.release_date, card.oracle_text, card.url, card.set_name, card.id))
        sql += ', '.join(values) + ') as c2(name, release_date, oracle_text, url, mtg_set, id) WHERE u2.id = u.id;'
        print(sql)
        cursor = database.cursor()
        cursor.execute(sql)
        database.commit()
        cursor.close()

    def insert_sets(self, mtg_sets: List[MTGSet]):
        if len(mtg_sets) < 1:
            return
        database = self.connect_to_database()
        format_string = '({}, {}, {}, {}, {})'
        sql = 'INSERT INTO mtg_set (name, code, release_date, card_count, set_type) VALUES '
        values = []
        for mtg_set in mtg_sets:
            values.append(format_string.format(mtg_set.name, mtg_set.code, mtg_set.release_date, mtg_set.card_count, mtg_set.set_type))
        sql += ', '.join(values) + ';'
        print(sql)
        cursor = database.cursor()
        cursor.execute(sql)
        database.commit()
        cursor.close()

    def update_sets(self, mtg_sets: List[MTGSet]):
        if len(mtg_sets) < 1:
            return
        database = self.connect_to_database()
        print(type(database))
        format_string = '({}, {}, {}, {}, {})'
        sql = 'UPDATE cards as c SET ' \
              'name = c2.name, ' \
              'code = c2.code, ' \
              'release_date = c2.release_date,' \
              'card_count = c2.card_count, ' \
              'set_type = c2.set_type FROM (VALUES'
        values = []
        for mtg_set in mtg_sets:
            values.append(format_string.format(mtg_set.name, mtg_set.code, mtg_set.release_date, mtg_set.card_count, mtg_set.set_type))
        sql += ', '.join(values) + ') as c2(name, code, release_date, card_count, set_type) WHERE u2.code = u.code;'
        print(sql)
        cursor = database.cursor()
        cursor.execute(sql)
        database.commit()
        cursor.close()
