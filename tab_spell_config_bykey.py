import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3
import os
from shared_state import SharedState

class SpellConfigTabByKey:
    def __init__(self, notebook, shared_state):
        self.frame = ttk.Frame(notebook)
        self.shared_state = shared_state
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.frame, columns=("Key Bind", "Spell Name"), show="headings")
        self.tree.heading("Key Bind", text="Key Bind")
        self.tree.heading("Spell Name", text="Spell Name")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        def on_edit(event):
            item = self.tree.focus()
            if item:
                current_values = self.tree.item(item, 'values')
                keybind = current_values[0]
                spell_name = simpledialog.askstring("Input", "Enter new spell name:", parent=self.frame)
                if spell_name is not None:
                    self.tree.item(item, values=(keybind, spell_name))
                    self.update_spell_name(keybind, spell_name)

        self.tree.bind('<Double-1>', on_edit)

        ttk.Button(self.frame, text="Create New Profile", command=self.create_profile).pack(padx=10, pady=(0, 10))

        ttk.Label(self.frame, text="Select Profile:").pack(padx=10, pady=(10, 0))
        self.profile_combo = ttk.Combobox(self.frame, values=self.get_profiles(), state="readonly")
        self.profile_combo.pack(padx=10, pady=(0, 10))
        self.profile_combo.bind("<<ComboboxSelected>>", self.on_profile_select)

    def create_new_profile(self, profile_name):
        if not profile_name:
            return
        database_name = f'{profile_name}.db'
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS spells (
                keybind TEXT PRIMARY KEY,
                spell_name TEXT
            )
        ''')
        conn.commit()
        conn.close()
        self.shared_state.current_profile = profile_name
        self.populate_initial_data(profile_name)
        self.load_data(profile_name)

    def populate_initial_data(self, profile_name):
        database_name = f'{profile_name}.db'
        tryme = {
            "ACTIONBUTTON1": ["1"],
            "ACTIONBUTTON2": ["2"],
            "ACTIONBUTTON3": ["3"],
            "ACTIONBUTTON4": ["4"],
            "ACTIONBUTTON5": ["5"],
            "ACTIONBUTTON6": ["Q"],
            "ACTIONBUTTON7": ["E"],
            "ACTIONBUTTON8": ["R"],
            "ACTIONBUTTON9": ["F"],
            "ACTIONBUTTON10": ["X"],
            "ACTIONBUTTON11": ["C"],
            "ACTIONBUTTON12": ["T"],

            "MULTIACTIONBAR1BUTTON1": ["^"],
            "MULTIACTIONBAR1BUTTON2": ["ALT-1"],
            "MULTIACTIONBAR1BUTTON3": ["ALT-2"],
            "MULTIACTIONBAR1BUTTON4": ["ALT-3"],
            "MULTIACTIONBAR1BUTTON6": ["CTRL-H"],
            "MULTIACTIONBAR1BUTTON7": ["CTRL-T"],
            "MULTIACTIONBAR1BUTTON8": ["SHIFT-Z"],
            "MULTIACTIONBAR1BUTTON9": ["V"],
            "MULTIACTIONBAR1BUTTON11": ["SHIFT-T"],
            "MULTIACTIONBAR1BUTTON12": ["F6"],

            "MULTIACTIONBAR2BUTTON1": ["SHIFT-1"],
            "MULTIACTIONBAR2BUTTON2": ["SHIFT-2"],
            "MULTIACTIONBAR2BUTTON3": ["SHIFT-3"],
            "MULTIACTIONBAR2BUTTON4": ["SHIFT-4"],
            "MULTIACTIONBAR2BUTTON5": ["SHIFT-5"],
            "MULTIACTIONBAR2BUTTON6": ["SHIFT-C"],
            "MULTIACTIONBAR2BUTTON7": ["SHIFT-E"],
            "MULTIACTIONBAR2BUTTON8": ["SHIFT-R"],
            "MULTIACTIONBAR2BUTTON9": ["SHIFT-F"],
            "MULTIACTIONBAR2BUTTON10": ["SHIFT-X"],
            "MULTIACTIONBAR2BUTTON11": ["SHIFT-Q"],
            "MULTIACTIONBAR2BUTTON12": ["G"],

            "MULTIACTIONBAR3BUTTON1": ["Y"],
            "MULTIACTIONBAR3BUTTON9": ["CTRL-1"],
            "MULTIACTIONBAR3BUTTON11": ["CTRL-3"],

            "MULTIACTIONBAR4BUTTON2": ["CTRL-5"],
            "MULTIACTIONBAR4BUTTON3": ["CTRL-F"],
            "MULTIACTIONBAR4BUTTON5": ["CTRL-Q"],
            "MULTIACTIONBAR4BUTTON6": ["CTRL-X"],
            "MULTIACTIONBAR4BUTTON8": ["CTRL-E"],
            "MULTIACTIONBAR4BUTTON9": ["CTRL-C"],
            "MULTIACTIONBAR4BUTTON10": ["CTRL-4"],
            "MULTIACTIONBAR4BUTTON11": ["CTRL-R"],
            "MULTIACTIONBAR4BUTTON12": ["CTRL-V"]
        }
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        for key, value in tryme.items():
            keybind = value[0]
            cursor.execute('''
                INSERT OR IGNORE INTO spells (keybind, spell_name)
                VALUES (?, ?)
            ''', (keybind, ""))
        conn.commit()
        conn.close()

    def fetch_data(self, profile_name):
        database_name = f'{profile_name}.db'
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM spells')
        data = cursor.fetchall()
        conn.close()
        return data

    def update_spell_name(self, keybind, spell_name):
        database_name = f'{self.shared_state.current_profile}.db'
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute('UPDATE spells SET spell_name = ? WHERE keybind = ?', (spell_name, keybind))
        conn.commit()
        conn.close()

    def load_data(self, profile_name):
        for i in self.tree.get_children():
            self.tree.delete(i)
        data = self.fetch_data(profile_name)
        for row in data:
            self.tree.insert("", "end", values=row)

    def create_profile(self):
        profile_name = simpledialog.askstring("Input", "Enter profile name:", parent=self.frame)
        if profile_name:
            if os.path.exists(f'{profile_name}.db'):
                messagebox.showerror("Error", "Profile already exists!")
            else:
                self.create_new_profile(profile_name)
                self.profile_combo['values'] = self.get_profiles()
                self.profile_combo.set(profile_name)

    def get_profiles(self):
        return [f.split('.db')[0] for f in os.listdir() if f.endswith('.db') and f != 'settings.db']

    def on_profile_select(self, event):
        selected_profile = self.profile_combo.get()
        if selected_profile:
            self.shared_state.current_profile = selected_profile
            self.load_data(self.shared_state.current_profile)