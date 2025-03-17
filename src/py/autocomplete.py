import tkinter as tk
from tkinter import ttk

class AutocompleteCombobox(ttk.Combobox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._completion_list = []
        self.bind('<KeyRelease>', self._on_keyrelease)

    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)
        self['values'] = self._completion_list

    def _on_keyrelease(self, event):
        value = self.get()
        if value == '':
            self['values'] = self._completion_list
        else:
            data = [item for item in self._completion_list if item.lower().startswith(value.lower())]
            self['values'] = data
