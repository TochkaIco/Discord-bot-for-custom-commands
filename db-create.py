import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

c.execute("""CREATE TABLE data (
        guild_id integer,
        commands text,
        text_from_command text
    )""")

conn.commit()
conn.close()