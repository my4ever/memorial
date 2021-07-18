import sqlite3
import os

from sqlite_tables import CREATE_TABLES


class MemorealDB():

    def __init__(self):

        # connecting to DB
        self.db = sqlite3.connect(os.path.join('', 'memoreal.db'))
        #  execution variable
        self.cursor =self.db.cursor()
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

db = sqlite3.connect('memoreal.db')
cursor = db.cursor()

def add_word_db(word):
    """Add word into database."""
    SQL = """INSERT INTO words_collection 
             (word) 
             VALUES (?)"""
    VALUES = (word,)
    cursor.execute(SQL, VALUES)
    db.commit()

def get_amount_db():
    """Getting the amount of words in database."""
    amount = cursor.execute(
        """SELECT id FROM words_collection
           ORDER BY id DESC 
           LIMIT 1"""
    ).fetchone()[0]
    return amount

def get_word_db(word_id):
    """Getting the word from database."""
    word = cursor.execute(
        'SELECT word FROM words_collection '
        f'WHERE id="{word_id}"'
    ).fetchone()[0]
    return word

def get_wordid_db(word):
    """Getting word id from database."""
    id = cursor.execute(
        'SELECT id FROM words_collection '
        f'WHERE word="{word}"'
    ).fetchone()[0]
    return id

def add_into_current_list_db(word):
    """Adding word into current list."""
    SQL = cursor.execute(
        '''INSERT INTO current_list 
           (word, db_id)
           VALUES (?, ?)'''
    )
    VALUES = (word, get_wordid_db(word))
    cursor.execute(SQL, VALUES)
    db.commit()

def get_current_list():
    """Getting current list."""
    current_words = cursor.execute(
        '''SELECT word FROM current_list'''
    ).fetchall()
    return current_words

def clear_current():
    cursor.execute(
        'DELETE FROM current_list'
    )
    db.commit()

