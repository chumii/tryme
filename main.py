import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('spell_data.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS spells (
        keybind TEXT PRIMARY KEY,
        spell_name TEXT
    )
''')

# Commit changes and close connection
conn.commit()
conn.close()

# # The provided dictionary data
# tryme = {
#     "ACTIONBUTTON1": ["1"],
#     "ACTIONBUTTON2": ["2"],
#     "ACTIONBUTTON3": ["3"],
#     "ACTIONBUTTON4": ["4"],
#     "ACTIONBUTTON5": ["5"],
#     "ACTIONBUTTON6": ["Q"],
#     "ACTIONBUTTON7": ["E"],
#     "ACTIONBUTTON8": ["R"],
#     "ACTIONBUTTON9": ["F"],
#     "ACTIONBUTTON10": ["X"],
#     "ACTIONBUTTON11": ["C"],
#     "ACTIONBUTTON12": ["T"],

#     "MULTIACTIONBAR1BUTTON1": ["^"],
#     "MULTIACTIONBAR1BUTTON2": ["ALT-1"],
#     "MULTIACTIONBAR1BUTTON3": ["ALT-2"],
#     "MULTIACTIONBAR1BUTTON4": ["ALT-3"],
#     "MULTIACTIONBAR1BUTTON6": ["CTRL-H"],
#     "MULTIACTIONBAR1BUTTON7": ["CTRL-T"],
#     "MULTIACTIONBAR1BUTTON8": ["SHIFT-Z"],
#     "MULTIACTIONBAR1BUTTON9": ["V"],
#     "MULTIACTIONBAR1BUTTON11": ["SHIFT-T"],
#     "MULTIACTIONBAR1BUTTON12": ["F6"],

#     "MULTIACTIONBAR2BUTTON1": ["SHIFT-1"],
#     "MULTIACTIONBAR2BUTTON2": ["SHIFT-2"],
#     "MULTIACTIONBAR2BUTTON3": ["SHIFT-3"],
#     "MULTIACTIONBAR2BUTTON4": ["SHIFT-4"],
#     "MULTIACTIONBAR2BUTTON5": ["SHIFT-5"],
#     "MULTIACTIONBAR2BUTTON6": ["SHIFT-C"],
#     "MULTIACTIONBAR2BUTTON7": ["SHIFT-E"],
#     "MULTIACTIONBAR2BUTTON8": ["SHIFT-R"],
#     "MULTIACTIONBAR2BUTTON9": ["SHIFT-F"],
#     "MULTIACTIONBAR2BUTTON10": ["SHIFT-X"],
#     "MULTIACTIONBAR2BUTTON11": ["SHIFT-Q"],
#     "MULTIACTIONBAR2BUTTON12": ["G"],

#     "MULTIACTIONBAR3BUTTON1": ["Y"],
#     "MULTIACTIONBAR3BUTTON9": ["CTRL-1"],
#     "MULTIACTIONBAR3BUTTON11": ["CTRL-3"],

#     "MULTIACTIONBAR4BUTTON2": ["CTRL-5"],
#     "MULTIACTIONBAR4BUTTON3": ["CTRL-F"],
#     "MULTIACTIONBAR4BUTTON5": ["CTRL-Q"],
#     "MULTIACTIONBAR4BUTTON6": ["CTRL-X"],
#     "MULTIACTIONBAR4BUTTON8": ["CTRL-E"],
#     "MULTIACTIONBAR4BUTTON9": ["CTRL-C"],
#     "MULTIACTIONBAR4BUTTON10": ["CTRL-4"],
#     "MULTIACTIONBAR4BUTTON11": ["CTRL-R"],
#     "MULTIACTIONBAR4BUTTON12": ["CTRL-V"]
# }

# # Insert data into the database
# def insert_data():
#     conn = sqlite3.connect('spell_data.db')
#     cursor = conn.cursor()

#     for key, value in tryme.items():
#         keybind = value[0]
#         cursor.execute('''
#             INSERT OR IGNORE INTO spells (keybind, spell_name)
#             VALUES (?, ?)
#         ''', (keybind, ""))

#     conn.commit()
#     conn.close()

# # Run the insert function
# insert_data()