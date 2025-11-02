import sqlite3
import os

# Build the absolute path dynamically
db_path = os.path.join(os.path.dirname(__file__), 'movies.sqlite')
print("Database path:", db_path)  # For debugging

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = cursor.fetchall()
print("Tables in the database:", tables)

if tables:
    for table in tables:
        table_name = table[0]
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
        count = cursor.fetchone()[0]
        print(f"Table '{table_name}' has {count} rows")

conn.close()
