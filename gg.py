import sqlite3

__connetions = None

def get_connetion():
    global __connetions
    if __connetions is None:
        __connetions = sqlite3.connect('Bubka.db')
    return __connetions

async  def init_db(force: bool = False):
    conn = get_connetion()
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS user_message')
    c.execute('''CREATE TABLE IF NOT EXISTS user_message(
                  id          INTEGER PRIMARY KEY,
                  user_id     INTEGER NOT NULL,
                  text        TEXT NOT NULL)
                   ''')
    conn.commit()




def add_message(user_id : int,text: str):
    conn = get_connetion()
    c = conn.cursor()
    c.execute('INSERT INTO user_message (user_id, text) VALUES (?,?)',(user_id, text))
    conn.commit()

if __name__ == '__main__':
    init_db()

    add_message(user_id=123,text='prosto')
