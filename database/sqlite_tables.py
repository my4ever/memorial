words_collection = '''CREATE TABLE IF NOT EXISTS words_collection(
                      id INTEGER PRIMARY KEY,
                      word TEXT DEFAULT ""
                      )'''

current_list = '''CREATE TABLE IF NOT EXISTS current_list(
                  id INTEGER PRIMARY KEY,
                  word TEXT DEFAULT ""
                  )'''

CREATE_TABLES = [words_collection, current_list]