import sqlite3

conn = sqlite3.connect("database/project.db")
cursor = conn.cursor()

# show all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

tables = cursor.fetchall()

print("Tables in database:")
for table in tables:
    print(table[0])

conn.close()