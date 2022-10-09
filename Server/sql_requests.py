import sqlite3

conn = sqlite3.connect('db\\data.db')
cur = conn.cursor()


def req(msg):
    try:
        if msg.split()[0].lower() == 'select':
            if msg.split()[1] == '*':
                return cur.execute(msg).fetchall(), True
            else:
                return cur.execute(msg).fetchone(), True
        else:
            cur.execute(msg)
            conn.commit()
            return False, None
    except Exception as error:
        return True, error
