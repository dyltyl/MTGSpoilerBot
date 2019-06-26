import psycopg2
import os


class DatabaseInstaller:
    def __init__(self):
        print('Connecting to db')
        parts = os.environ['DATABASE_URL'].split(":")
        self.username = parts[1][2:]
        self.password = parts[2][0:parts[2].index("@")]
        self.database = parts[3][parts[3].index("/") + 1:]
        self.path = os.path.realpath(__file__)
        try:
            self.path = self.path[0:self.path.rindex('/')]
        except ValueError:
            self.path = self.path[0:self.path.rindex('\\')]
        print('username: ' + self.username)
        print('password: ' + self.password)
        print('database: ' + self.database)
        print('path: ' + self.path)

    def start_db(self):
        os.system('service postgresql start')

    def connect_to_database(self): #Todo: add null checks/etc
        return psycopg2.connect("dbname="+self.database+" user="+self.username+" password="+self.password)

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
            cursor.close()
        else:
            print(tablename + ' needs updating')

    def setup_tables(self):
        self.start_db()
        self.create_table('MTG_Set', self.path+'/MTG_Set.sql')
        self.create_table('Cards', self.path + '/Cards.sql')

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
