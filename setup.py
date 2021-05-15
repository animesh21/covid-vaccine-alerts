import json
import sqlite3

from constants import DB_NAME

TABLE_NAMES = ['states', 'districts', 'users']
INITIAL_DATA_FILE = 'initial_data.json'


def create_tables():
    # connect with database and check if tables exist, if not create new ones
    with sqlite3.connect(DB_NAME) as con:
        con.execute('PRAGMA foreign_keys = 1')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS states (id INTEGER NOT NULL PRIMARY KEY, name TEXT)')
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS districts
            (
                id INTEGER NOT NULL PRIMARY KEY,
                state_id INTEGER NOT NULL,
                name TEXT,
                FOREIGN KEY (state_id) REFERENCES states(id)
            )'''
        )
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS users
            (
                id INTEGER NOT NULL PRIMARY KEY,
                district_id INTEGER NOT NULL,
                name TEXT,
                phone TEXT,
                is_active INTEGER,
                last_notified TEXT,
                FOREIGN KEY (district_id) REFERENCES districts(id)
            )'''
        )

        # save the changes in the db
        con.commit()


def load_data():
    # get a db connection
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()

        # load data from the file and load into database
        with open(INITIAL_DATA_FILE, 'rb') as fp:
            data = json.load(fp)
            states = data['states']
            districts = data['districts']
            sql_insert_statement_for_states = 'INSERT INTO states VALUES (:id, :name)'
            sql_insert_statement_for_districts = 'INSERT INTO districts VALUES (:id, :state_id, :name)'
            cur.executemany(sql_insert_statement_for_states, states)
            cur.executemany(sql_insert_statement_for_districts, districts)
        con.commit()


if __name__ == '__main__':
    print('Creating tables ...')
    create_tables()
    print('Successfully created tables')
    print(f'Now populating with initial data from {INITIAL_DATA_FILE} ...')
    load_data()
    print('Data populated successfully')
