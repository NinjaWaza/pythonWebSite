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

    # Getter

    def get_db(self):
        return self.db

    # Setter

    def set_db(self, _value):
        pass

    # Destructor

    def close_db(self):
        if self.m_db is not None:
            self.m_db.close()

    # Properties

    db = property(get_db, set_db, close_db)

    # ##############
    # ## METHODS
    # ##############

    def select_one(self, _query, _params=None):
        """ Return a sqlite3 row with query result or 'Error' is something goes wrong """
        try:
            cursor = self.m_db.cursor()

            if _params is not None:
                return cursor.execute(_query, _params).fetchone()
            else:
                return cursor.execute(_query).fetchone()

        except sqlite3.Error as error:
            return Database.compute_sqlite3_error(error)

    def select_all(self, _query, _params=None):
        """ Return array of sqlite3 row with query result or 'Error' is something goes wrong """
        try:
            cursor = self.m_db.cursor()

            if _params is not None:
                return cursor.execute(_query, _params).fetchall()
            else:
                return cursor.execute(_query).fetchall()
        except sqlite3.Error as error:
            return Database.compute_sqlite3_error(error)

    def update(self, _query, _params=None):
        """ Handle update query on Database, return "Error" if something goes wrong """
        try:
            cursor = self.m_db.cursor()
            cursor.execute(_query, _params)
            self.m_db.commit()
        except sqlite3.Error as error:
            return Database.compute_sqlite3_error(error)

    def delete(self, _query, _params=None):
        """ Handle delete query on Database, return "Error" if something goes wrong """
        self.update(_query, _params)

    def add(self, _query, _params=None):
        """ Handle specific add update query on Database """
        self.update(_query, _params)

    # ##############
    # ## STATICS
    # ##############

    @staticmethod
    def compute_sqlite3_error(_error):
        print('SQLite error: %s' % (' '.join(_error.args)))
        print("Exception class is: ", _error.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
        return "Error"

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
