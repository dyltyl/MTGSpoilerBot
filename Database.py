import psycopg2
import os


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

    def connect_to_database(self): #Todo: add null checks/etc
        return psycopg2.connect("dbname="+self.database+" user="+self.username+" password="+self.password + " host="+self.host + " port="+self.port)

    def check_table_exists(self, table):
        database = self.connect_to_database()
        cursor = database.cursor()
        cursor.execute("SELECT 1 FROM information_schema.tables WHERE table_name = '"+table+"';")
        result = cursor.fetchone()
        cursor.close()
        database.close()
        if result is None:
            return False
        return True

    def create_table(self, tablename, filename):
        if not self.check_table_exists(tablename):
            database = self.connect_to_database()
            sql_file = open(filename, "r")
            sql = sql_file.read()
            sql_file.close()
            cursor = database.cursor()
            cursor.execute(sql)
            #database.commit()
            cursor.close()
            #database.close()
        else:
            print(tablename + ' needs updating')

    def setup_tables(self):
        #self.start_db()
        self.create_table('mtg_set', self.path+'/MTG_Set.sql')
        print('Created MTG_Set', self.check_table_exists('mtg_set'))
        self.create_table('cards', self.path + '/Cards.sql')

    def verify_tables(self):
        database = self.connect_to_database()
        cursor = database.cursor()
        cursor.execute('SELECT pg_tables.tablename FROM pg_catalog.pg_tables;')
        row = cursor.fetchone()
        tables = []
        while row is not None:
            tables.append(row[0])
            row = cursor.fetchone()
        expected_tables = ['players', 'commander_damage', 'games', 'commanders', 'life']
        for table in expected_tables:
            if table not in tables:
                raise Exception(table + ' table missing from installation')
