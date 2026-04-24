import sqlite3
def player_info():
    with sqlite3.connect('chat_history.db') as db:
        cursor = db.cursor()
        cursor.execute('''
    CREATE TABLE IF NOT EXISTS player_info(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    hp INTEGER,
    exp INTEGER,
    gold INTEGER,
    inventory TEXT,
    chat_id INTEGER,
    user_message TEXT,
    ai_message TEXT,
    role TEXT)
    ''')
def save_message(chat_id,hp=None, exp=None, gold=None, inventory=None, user_message=None, ai_message=None,role=None): #Сохранять данные
    with sqlite3.connect('chat_history.db') as db:
        cursor = db.cursor()
        cursor.execute('INSERT INTO player_info(user_id,hp, exp, gold, inventory, chat_id, user_message, ai_message, role) VALUES (?,?,?,?,?,?,?,?,?) ',(chat_id,hp, exp, gold, inventory, chat_id, user_message, ai_message,role))
def export_message(chat_id): #добавлять
    with sqlite3.connect('chat_history.db') as db:
        db.row_factory=sqlite3.Row
        cursor = db.cursor()
        cursor.execute('SELECT * from player_info where chat_id = ?',(chat_id,))
        rows=cursor.fetchall()
        spisok=[]
        for row in rows:
            spisok.append(dict(row))
        return spisok
#player_info()