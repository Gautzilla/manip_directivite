import customtkinter as ctk

class BirthDate(ctk.CTkFrame):

    year_v: int
    month_v: int
    day_v: int

    monthes = {'Janvier': 1, 'Février': 2, 'Mars': 3, 'Avril': 4, 'Mai': 5, 'Juin': 6, 'Juillet': 7, 'Août': 8, 'Septembre': 9, 'Octobre': 10, 'Novembre': 11, 'Décembre': 12}

    def set_day(self, callback: str):
        self.day_v = int(callback)

    def set_month(self, callback: str):
        self.month_v = self.monthes[callback]

    def set_year(self, callback: str):
        self.year_v = int(callback)

    def get_birthdate(self) -> tuple:
        return (self.day_v, self.month_v, self.year_v)

    def __init__(self, master):
        super().__init__(master)

        self.day = 0

        birthdate_header = ctk.CTkLabel(master = self, text = 'Date de naissance')
        birthdate_header.grid(column = 1, row = 0, padx = 0, pady = 0, sticky = 'new')

        self.grid_columnconfigure([0,2], weight = 1)

        day = ctk.CTkComboBox(master = self, width = 100, values = [str(x) for x in range(1,32)], command = self.set_day, state = 'readonly')
        day.grid(column = 0, row = 1, padx=(10,0), pady = 10, sticky = 'ew')
        day.set('Jour')

        month = ctk.CTkComboBox(master = self, width = 100, values = [key for key in self.monthes.keys()], command = self.set_month, state = 'readonly')
        month.grid(column = 1, row = 1, padx=(10,0), pady = 10, sticky = 'ew')
        month.set('Mois')

        year = ctk.CTkComboBox(master = self, width = 100, values = [str(x) for x in range(1960, 2011)], command = self.set_year, state = 'readonly')
        year.grid(column = 2, row = 1, padx=10, pady = 10, sticky = 'ew')
        year.set('Année')


class LoginView(ctk.CTkFrame):

    def submit(self, birth_date: BirthDate, first_name: ctk.CTkEntry, last_name: ctk.CTkEntry):
        day, month, year = birth_date.get_birthdate()
        first_name = first_name.get()
        last_name = last_name.get()
        pass

    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure([0,2], weight = 1)

        first_name = ctk.CTkEntry(master = self, placeholder_text = 'Prénom')
        first_name.grid(column = 1, row = 0, padx = 40, pady = (10,0), sticky = 'ew')

        last_name = ctk.CTkEntry(master = self, placeholder_text = 'Nom')
        last_name.grid(column = 1, row = 1, padx = 40, pady = (10,0), sticky = 'ew')

        birth_date = BirthDate(master = self)
        birth_date.grid(column = 1, row = 2, padx = 10, pady = (10,0), sticky = 'new')

        submit = ctk.CTkButton(master = self, width = 100, text = 'Valider', command = lambda: self.submit(birth_date = birth_date, first_name = first_name, last_name = last_name))
        submit.grid(column = 1, row = 3, padx = 0, pady = (10, 0), sticky = 'new')