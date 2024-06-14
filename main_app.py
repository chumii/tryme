import tkinter as tk
from tkinter import ttk
from tab_spell_config_bykey import SpellConfigTabByKey
from tab_spell_config_byspell import SpellConfigTabBySpell
from tab_settings import SettingsTab
from tab_run import RunTab
from shared_state import SharedState

# Create the main application window
app = tk.Tk()
app.title("tryme")

# Create a Notebook widget (tabbed interface)
notebook = ttk.Notebook(app)
notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a shared state object
shared_state = SharedState()

# Add the Spell Configuration tab
spell_config_tab = SpellConfigTabByKey(notebook, shared_state)
notebook.add(spell_config_tab.frame, text="Spell Configuration")

# Add the Spell Configuration by Spell tab
spell_config_tab_byspell = SpellConfigTabBySpell(notebook, shared_state)
notebook.add(spell_config_tab_byspell.frame, text="Spell Configuration by Spell")

# Add the Settings tab
settings_tab = SettingsTab(notebook, shared_state)
notebook.add(settings_tab.frame, text="Settings")

run_tab = RunTab(notebook, shared_state)
notebook.add(run_tab.frame, text="Letsgo!")

# Run the main application loop
app.mainloop()
