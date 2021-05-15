import sqlite3
from datetime import datetime

from constants import DATETIME_FORMAT, DB_NAME


def get_active_users(district_id=None):
    """
    Returns list of dict with each dict containing data of an active user
    :param district_id: int, district id of the district from which the users have to be returned
    :return: list of user dict
    """
    # get the db connection
    with sqlite3.connect(DB_NAME) as con:
        con.row_factory = sqlite3.Row  # to get an sql row as a Python dictionary
        cur = con.cursor()
        if district_id:
            sql_query = 'SELECT * FROM users WHERE is_active = ? AND district_id = ?'
            active_users = [dict(row) for row in cur.execute(sql_query, (True, district_id))]
        else:
            sql_query = 'SELECT * FROM users WHERE is_active = ?'
            active_users = [dict(row) for row in cur.execute(sql_query, (True, ))]
    return active_users


def get_active_district_ids():
    """
    Queries unique district ids of active users
    :return: list of unique district ids
    """
    # get the db connection
    with sqlite3.connect(DB_NAME) as con:
        con.row_factory = sqlite3.Row  # to get an sql row as a Python dictionary
        cur = con.cursor()
        active_district_ids = [
            dict(row)['district_id'] for row in
            cur.execute('SELECT DISTINCT district_id FROM users WHERE is_active = ?', (True, )).fetchall()
        ]
    return active_district_ids


def update_last_notified(user_id):
    """
    Updates row with id=user_id in users table with current time as last_notified column value
    :param user_id: id of the user for which last_notified is to be updated
    :return: None
    """
    now_str = datetime.now().strftime(DATETIME_FORMAT)
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute('UPDATE users SET last_notified = ? WHERE id = ?', (now_str, user_id))
