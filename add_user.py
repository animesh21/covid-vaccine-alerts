import sqlite3

from constants import DB_NAME


def add_user():
    # create a db connection
    with sqlite3.connect(DB_NAME) as con:
        # get the cursor to execute queries
        cur = con.cursor()

        # get the user data from the user
        name = input("Please enter name of the user: ")
        phone = str(input("Please enter 10 digit phone number of the user: ")).strip()
        phone = '+91' + phone[-10:]  # make it in international format

        print("Please select state of the user from the list below and enter the id of state:")
        for row in cur.execute('SELECT id, name FROM states'):
            print('{:<3}: {}'.format(*row))
        state_id = int(input())

        print("Please select the district of the user from the list below and enter the id of district:")
        for row in cur.execute('SELECT id, name FROM districts WHERE state_id = ?', (state_id, )):
            print('{:<3}: {}'.format(*row))
        district_id = int(input())
        cur.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)', (None, district_id, name, phone, True, None))
        con.commit()


if __name__ == '__main__':
    add_user()
