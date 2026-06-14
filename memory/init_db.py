import sqlite3

conn = sqlite3.connect('memory/short_term.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS memory (key TEXT PRIMARY KEY, value TEXT)')
conn.commit()
conn.close()
print("Short-term memory initialized")