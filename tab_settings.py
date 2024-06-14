import tkinter as tk
from tkinter import ttk
import sqlite3
from shared_state import SharedState

class SettingsTab:
    def __init__(self, notebook, shared_state):
        self.frame = ttk.Frame(notebook)
        self.shared_state = shared_state
        self.create_widgets()
        self.init_db()
        self.load_settings()

        # Register a callback to update the current profile label
        self.shared_state.register_callback(self.update_current_profile)

    def create_widgets(self):
        ttk.Label(self.frame, text="Current Profile:").pack(padx=10, pady=(10, 0))
        self.current_profile_label = ttk.Label(self.frame, text="")
        self.current_profile_label.pack(padx=10, pady=(0, 10))

        hekili_frame = ttk.LabelFrame(self.frame, text="Hekili Position")
        hekili_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(hekili_frame, text="X Coordinate:").grid(row=0, column=0, padx=5, pady=5)
        self.x_coord_entry = ttk.Entry(hekili_frame)
        self.x_coord_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(hekili_frame, text="Y Coordinate:").grid(row=1, column=0, padx=5, pady=5)
        self.y_coord_entry = ttk.Entry(hekili_frame)
        self.y_coord_entry.grid(row=1, column=1, padx=5, pady=5)

        save_button = ttk.Button(hekili_frame, text="Save Settings", command=self.save_settings)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

    def update_current_profile(self, profile_name):
        self.current_profile_label.config(text=profile_name if profile_name else "None")

    def init_db(self):
        conn = sqlite3.connect('settings.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                name TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save_settings(self):
        x_coord = self.x_coord_entry.get()
        y_coord = self.y_coord_entry.get()

        conn = sqlite3.connect('settings.db')
        cursor = conn.cursor()
        cursor.execute('REPLACE INTO settings (name, value) VALUES (?, ?)', ('hekili_x', x_coord))
        cursor.execute('REPLACE INTO settings (name, value) VALUES (?, ?)', ('hekili_y', y_coord))
        conn.commit()
        conn.close()

    def load_settings(self):
        conn = sqlite3.connect('settings.db')
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM settings WHERE name = ?', ('hekili_x',))
        x_coord = cursor.fetchone()
        cursor.execute('SELECT value FROM settings WHERE name = ?', ('hekili_y',))
        y_coord = cursor.fetchone()
        conn.close()

        if x_coord:
            self.x_coord_entry.insert(0, x_coord[0])
        if y_coord:
            self.y_coord_entry.insert(0, y_coord[0])
