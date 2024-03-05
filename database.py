import sqlite3
conn = sqlite3.connect('69.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS selected_path (
                  id INTEGER PRIMARY KEY,
                   path TEXT
                )''')

conn.commit()

cursor.close()
conn.close()
