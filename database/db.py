import sqlite3
import os

from .sqlite_tables import CREATE_TABLES


class MemorealDB():

    def __init__(self):

        # connecting to DB
        self.db = sqlite3.connect(os.path.join('database', 'memoreal.db'))
        #  execution variable
        self.cursor = self.db.cursor()
        for table in CREATE_TABLES:
            if self.cursor.execute("SELECT name FROM sqlite_master "
                                   f"WHERE type='table' AND name='{table}'").fetchall():
                print('It`s ok - db exists')
            else:
                print(f'Have to create table: {table.split()[5].strip("(")}')
                self.cursor.execute(table)
            print('connection closed')
        self.db.close()


MemorealDB()


def add_word_db(word):
    """Add word into database."""
    db = sqlite3.connect('database/memoreal.db')
    cursor = db.cursor()
    SQL = """INSERT INTO words_collection 
             (word) 
             VALUES (?)"""
    VALUES = (word,)
    cursor.execute(SQL, VALUES)
    db.commit()
    db.close()


def get_amount_db():
    db = sqlite3.connect('database/memoreal.db')
    cursor = db.cursor()
    """Getting the amount of words in database."""
    amount = cursor.execute(
        """SELECT id FROM words_collection
           ORDER BY id DESC 
           LIMIT 1"""
    ).fetchone()[0]
    db.close()
    return amount


def get_word_db(word_id):
    """Getting the word from database."""
    db = sqlite3.connect('database/memoreal.db')
    cursor = db.cursor()
    word = cursor.execute(
        'SELECT word FROM words_collection '
        f'WHERE id="{word_id}"'
    ).fetchone()[0]
    db.close()
    return word


def get_wordid_db(word):
    """Getting word id from database."""
    db = sqlite3.connect('database/memoreal.db')
    cursor = db.cursor()
    id = cursor.execute(
        'SELECT id FROM words_collection '
        f'WHERE word="{word}"'
    ).fetchone()[0]
    db.close()
    return id


def add_into_current_list_db(word):
    """Adding word into current list."""
    db = sqlite3.connect('database/memoreal.db')
    cursor = db.cursor()
    SQL = '''INSERT INTO current_list 
           (word)
           VALUES(?)'''
    VALUES = word
    cursor.execute(SQL, [VALUES])
    db.commit()
    db.close()


def get_current_list():
    """Getting current list."""
    db = sqlite3.connect('database/memoreal.db')
    cursor = db.cursor()
    current_words = [word[0] for word in cursor.execute(
        '''SELECT word FROM current_list'''
    ).fetchall()]
    db.close()
    return current_words


def get_current_word_db(word_id):
    """Getting the word from current list."""
    db = sqlite3.connect('database/memoreal.db')
    cursor = db.cursor()
    word = cursor.execute(
        'SELECT word FROM current_list '
        f'WHERE id="{word_id}"'
    ).fetchone()[0]
    db.close()
    return word


def get_current_amount_db():
    """Getting the amount of words in current list."""
    db = sqlite3.connect('database/memoreal.db')
    cursor = db.cursor()
    amount = cursor.execute(
        """SELECT id FROM current_list"""
    ).fetchall()
    db.close()
    return amount


def get_current_wordid_db(word):
    """Getting word id from database."""
    db = sqlite3.connect('database/memoreal.db')
    cursor = db.cursor()
    id = cursor.execute(
        'SELECT id FROM current_list '
        f'WHERE word="{word}"'
    ).fetchone()
    db.commit()
    return id


def clear_current_db():
    db = sqlite3.connect('database/memoreal.db')
    cursor = db.cursor()
    cursor.execute(
        'DELETE FROM current_list'
    )
    db.commit()
    db.close()
