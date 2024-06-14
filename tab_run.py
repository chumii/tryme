import tkinter as tk
from tkinter import ttk
import sqlite3
from shared_state import SharedState

class RunTab:
    def __init__(self, notebook, shared_state):
        self.frame = ttk.Frame(notebook)
        self.shared_state = shared_state
        self.create_widgets()

       

    def create_widgets(self):

        run_frame = ttk.LabelFrame(self.frame, text="Try me!")
        run_frame.pack(padx=10, pady=10, fill="x")

        save_button = ttk.Button(run_frame, text="Run!", command=self.tryme)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

    
    def tryme(self):
       print("try me!")

