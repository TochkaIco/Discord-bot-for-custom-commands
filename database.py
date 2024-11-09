import sqlite3

db_file_name = 'data.db'

# Query the DB and Return All Records
def show_all():
    global db_file_name
    conn = sqlite3.connect(db_file_name)
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM data")
    items = c.fetchall()
    conn.commit()
    conn.close()
    return items

def show_all_server_specific(guild_id):
    global db_file_name
    conn = sqlite3.connect(db_file_name)
    c = conn.cursor()
    c.execute("SELECT commands, text_from_command FROM data WHERE guild_id = (?)", (guild_id,))
    info = c.fetchall()
    conn.commit()
    conn.close()
    return info

# Add A New Record To The Table
def add_record(record_info):
    global db_file_name
    conn = sqlite3.connect(db_file_name)
    c = conn.cursor()
    c.execute("INSERT INTO data VALUES (?, ?, ?)", record_info)
    conn.commit()
    conn.close()

def delete_record(guild_id, command):
    global db_file_name
    conn = sqlite3.connect(db_file_name)
    c = conn.cursor()
    if command_check(guild_id, command) == 'exists':
        c.execute("DELETE FROM data WHERE guild_id = (?) AND commands = (?)", (guild_id, command))
        conn.commit()
        conn.close()
    else:
        conn.commit()
        conn.close()
        return 'There is no command with this name on your server'

# Looks For A Specific Command
def command_lookup(guild_id, command):
    global db_file_name
    conn = sqlite3.connect(db_file_name)
    c = conn.cursor()
    c.execute("SELECT text_from_command FROM data WHERE guild_id = (?) AND commands = (?)", (guild_id, command))
    info = c.fetchone()
    conn.commit()
    conn.close()
    return info

# Checks If A guild_id Is Saved In DB
def guildID_check(guild_id):
    global db_file_name
    conn = sqlite3.connect(db_file_name)
    c = conn.cursor()
    c.execute("SELECT EXISTS(SELECT 1 FROM data WHERE guild_id = ?)", (guild_id,))
    exists = c.fetchone()
    conn.commit()
    conn.close()
    if exists:
        return 'exists'
    else:
        return 'not found'
    
# Checks If A command Is Saved In DB
def command_check(guild_id, command):
    global db_file_name
    conn = sqlite3.connect(db_file_name)
    c = conn.cursor()
    c.execute("SELECT EXISTS(SELECT 1 FROM data WHERE guild_id = (?) and commands = (?) )", (guild_id, command))
    exists = c.fetchone()
    conn.commit()
    conn.close()
    if exists:
        return 'exists'
    else:
        return 'not found'