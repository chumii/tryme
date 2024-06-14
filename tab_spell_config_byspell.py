import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3
import os
from shared_state import SharedState
from spells import trymespells

class SpellConfigTabBySpell:
    def __init__(self, notebook, shared_state):
        self.frame = ttk.Frame(notebook)
        self.shared_state = shared_state
        self.create_widgets()
        self.keybind = ""

    def create_widgets(self):
        self.tree = ttk.Treeview(self.frame, columns=("Spell Name", "Key Bind"), show="headings")
        self.tree.heading("Spell Name", text="Spell Name")
        self.tree.heading("Key Bind", text="Key Bind")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Bind the double-click event
        self.tree.bind('<Double-1>', self.on_edit)

        ttk.Button(self.frame, text="Create New Profile", command=self.create_profile).pack(padx=10, pady=(0, 10))

        ttk.Label(self.frame, text="Select Profile:").pack(padx=10, pady=(10, 0))
        self.profile_combo = ttk.Combobox(self.frame, values=self.get_profiles(), state="readonly")
        self.profile_combo.pack(padx=10, pady=(0, 10))
        self.profile_combo.bind("<<ComboboxSelected>>", self.on_profile_select)

    def on_edit(self, event):
        # Get the selected item
        item = self.tree.selection()
        if item:
            item = item[0]
            current_values = self.tree.item(item, 'values')
            spell_name = current_values[0]
            self.open_keybind_popup(item, spell_name)

    def open_keybind_popup(self, item, spell_name):
        self.keybind = ""
        popup = tk.Toplevel(self.frame)
        popup.title("Capture Key Bind")
        popup.geometry("300x150")

        label = ttk.Label(popup, text="Press 'Capture' to start key capturing")
        label.pack(pady=10)

        def start_capture():
            label.config(text="Press the key combination")
            popup.bind("<KeyPress>", on_key_press)
            popup.bind("<KeyRelease>", on_key_release)

        def on_key_press(event):
            key = self.format_key(event)
            if key:
                if key not in self.keybind.split('+'):
                    self.keybind = "+".join(filter(None, [self.keybind, key]))
                    label.config(text=f"Captured: {self.keybind}")

        def on_key_release(event):
            # Allow capturing of more keys
            pass

        def on_ok():
            self.tree.item(item, values=(spell_name, self.keybind))
            self.update_key_bind(spell_name, self.keybind)
            popup.destroy()

        def on_close():
            self.tree.item(item, values=(spell_name, self.keybind))
            self.update_key_bind(spell_name, self.keybind)
            popup.destroy()

        ttk.Button(popup, text="Capture", command=start_capture).pack(pady=5)
        ttk.Button(popup, text="Close", command=on_close).pack(pady=5)

    def format_key(self, event):
        key = event.keysym
        if key in ['Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R']:
            return ""
        modifiers = []
        if event.state & 0x0001:  # Shift
            modifiers.append("Shift")
        if event.state & 0x0004:  # Control
            modifiers.append("Ctrl")
        if event.state & 0x20000:  # Alt
            modifiers.append("Alt")
        return "-".join(modifiers + [key])

    def create_new_profile(self, profile_name):
        if not profile_name:
            return
        database_name = f'{profile_name}_byspell.db'
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS spells (
                spell_name TEXT PRIMARY KEY,
                keybind TEXT
            )
        ''')
        conn.commit()
        conn.close()
        self.shared_state.current_profile = profile_name
        self.populate_initial_data(profile_name)
        self.load_data(profile_name)

    def populate_initial_data(self, profile_name):
        database_name = f'{profile_name}_byspell.db'
        # trymespells = [
        #     "Barbed Shot",
        #     "Bestial Wrath",
        #     "Multi Shot"
        # ]
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        for spell in trymespells:
            cursor.execute('''
                INSERT OR IGNORE INTO spells (spell_name, keybind)
                VALUES (?, ?)
            ''', (spell, ""))
        conn.commit()
        conn.close()

    def fetch_data(self, profile_name):
        database_name = f'{profile_name}_byspell.db'
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM spells')
        data = cursor.fetchall()
        conn.close()
        return data

    def update_key_bind(self, spell_name, keybind):
        database_name = f'{self.shared_state.current_profile}_byspell.db'
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute('UPDATE spells SET keybind = ? WHERE spell_name = ?', (keybind, spell_name))
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
            if os.path.exists(f'{profile_name}_byspell.db'):
                messagebox.showerror("Error", "Profile already exists!")
            else:
                self.create_new_profile(profile_name)
                self.profile_combo['values'] = self.get_profiles()
                self.profile_combo.set(profile_name)

    def get_profiles(self):
        return [f.split('_byspell.db')[0] for f in os.listdir() if f.endswith('_byspell.db')]

    def on_profile_select(self, event):
        selected_profile = self.profile_combo.get()
        if selected_profile:
            self.shared_state.current_profile = selected_profile
            self.load_data(self.shared_state.current_profile)
