import sqlite3
import sys
import traceback

import click
from flask import current_app
from flask.cli import with_appcontext


class Database:

    def __init__(self):
        self.m_db = sqlite3.connect("database.db")
        self.m_db.row_factory = sqlite3.Row

    def get_db(self):
        return self.db

    def set_db(self, _value):
        pass

    def select_one(self, _query, _params=None):
        """ Return sqlit3 row with query result or 'Error' is something goes wrong """
        try:
            cursor = self.m_db.cursor()

            if _params is not None:
                return cursor.execute(_query, _params).fetchone()
            else:
                return cursor.execute(_query).fetchone()

            print("try done")
        except sqlite3.Error as error:
            print('SQLite error: %s' % (' '.join(error.args)))
            print("Exception class is: ", error.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            return None

    def select_all(self, _query, _params=None):
        """ Return array of sqlit3 row with query result or 'Error' is something goes wrong """
        try:
            cursor = self.m_db.cursor()

            if _params is not None:
                return cursor.execute(_query, _params).fetchall()
            else:
                return cursor.execute(_query).fetchall()
        except sqlite3.Error as error:
            print('SQLite error: %s' % (' '.join(error.args)))
            print("Exception class is: ", error.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            return "Error"

    def update(self, _query, _params=None):
        """ Return array of sqlit3 row with query result or 'Error' is something goes wrong """
        try:
            cursor = self.m_db.cursor()
            cursor.execute(_query, _params)
            self.m_db.commit()
        except sqlite3.Error as error:
            print('SQLite error: %s' % (' '.join(error.args)))
            print("Exception class is: ", error.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            return "Error"

    def delete(self, _query, _params=None):
        """ Return array of sqlit3 row with query result or 'Error' is something goes wrong """
        self.update(_query, _params)

    def add(self, _query, _params=None):
        """ Return array of sqlit3 row with query result or 'Error' is something goes wrong """
        self.update(_query, _params)

    def close_db(self):
        if self.m_db is not None:
            self.m_db.close()

    db = property(get_db, set_db, close_db)

    @staticmethod
    @click.command(name="init-db")
    @with_appcontext
    def init_db_command():
        """Clear the existing data and create new tables."""

        connexion = sqlite3.connect("database.db")
        click.echo('Opened database successfully')

        with current_app.open_resource('schema.sql') as file:
            connexion.executescript(file.read().decode("utf8"))
            click.echo('Database initiate successfully')
