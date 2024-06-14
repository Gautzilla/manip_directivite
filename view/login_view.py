import customtkinter as ctk
from datetime import date

class BirthDate(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        day = ctk.CTkComboBox(master = self, width = 60, values = [str(x) for x in range(1,32)])
        day.grid(column = 0, row = 0, padx=(10,0), pady = (10,0), sticky = 'ew')

        month = ctk.CTkComboBox(master = self, width = 100, values = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'])
        month.grid(column = 1, row = 0, padx=(10,0), pady = (10,0), sticky = 'ew')

        year = ctk.CTkComboBox(master = self, width = 70, values = [str(x) for x in range(1960, 2011)])
        year.grid(column = 2, row = 0, padx=(10,0), pady = (10,0), sticky = 'ew')


class LoginView(ctk.CTkFrame):

    user_first_name = ''
    user_last_name = ''
    user_birth_date = date(year = 2000, month = 1, day = 1)

    def __init__(self, master):
        super().__init__(master)

        first_name = ctk.CTkEntry(master = self, placeholder_text = 'Prénom')
        first_name.grid(column = 0, row = 0, padx = (10,0), pady = (10,0), sticky = 'ew')

        last_name = ctk.CTkEntry(master = self, placeholder_text = 'Nom')
        last_name.grid(column = 1, row = 0, padx = (10,0), pady = (10,0), sticky = 'ew')

        birth_date = BirthDate(master = self)
        birth_date.grid(column = 0, row = 1, padx = (10,0), pady = (10,0), sticky = 'new')