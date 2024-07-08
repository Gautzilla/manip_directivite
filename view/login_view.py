import customtkinter as ctk

class BirthDate(ctk.CTkFrame):

    year_v = 0
    month_v = 0
    day_v = 0

    monthes = {'Janvier': 1, 'Février': 2, 'Mars': 3, 'Avril': 4, 'Mai': 5, 'Juin': 6, 'Juillet': 7, 'Août': 8, 'Septembre': 9, 'Octobre': 10, 'Novembre': 11, 'Décembre': 12}

    def get_birthdate(self) -> tuple:
        return (self.day_v.get(), self.month_v.get(), self.year_v.get())
    
    def set_month(self, callback: str):
        self.month_v = ctk.StringVar(value = self.monthes[callback])

    def __init__(self, master):
        super().__init__(master)

        self.day_v = ctk.StringVar(value = 'Jour')
        self.month_v = ctk.StringVar(value = 'Mois')
        self.year_v = ctk.StringVar(value = 'Année')

        birthdate_header = ctk.CTkLabel(master = self, text = 'Date de naissance')
        birthdate_header.grid(column = 1, row = 0, padx = 0, pady = 0, sticky = 'new')

        self.grid_columnconfigure([0,2], weight = 1)

        day = ctk.CTkComboBox(master = self, width = 100, values = [str(x) for x in range(1,32)], variable = self.day_v)
        day.grid(column = 0, row = 1, padx=(10,0), pady = 10, sticky = 'ew')
        day.set('Jour')

        month = ctk.CTkComboBox(master = self, width = 100, values = [key for key in self.monthes.keys()], variable = self.month_v, command = self.set_month)
        month.grid(column = 1, row = 1, padx=(10,0), pady = 10, sticky = 'ew')
        month.set('Mois')

        year = ctk.CTkComboBox(master = self, width = 100, values = [str(x) for x in range(1960, 2011).__reversed__()], variable = self.year_v)
        year.grid(column = 2, row = 1, padx=10, pady = 10, sticky = 'ew')
        year.set('Année')

class LoadSessionView(ctk.CTkFrame):
    def __init__(self, master, controller, users: dict):
        super().__init__(master)

        self.grid_columnconfigure((0,2), weight = 1)

        self.users = users
        self.selected_user = ctk.StringVar(value = '')

        self.controller = controller

        self.user_names = ctk.CTkOptionMenu(master = self, width = 200, values = list(users.keys()), variable = self.selected_user, command = self.activate_button)
        self.user_names.grid(column = 1, row = 0, padx = 10, pady = (10, 0), sticky = 'new')

        self.recall_user = ctk.CTkButton(master = self, width = 100, text = 'Charger Session', command = self.load_session, state = 'disabled')
        self.recall_user.grid(column = 1, row = 1, padx = 10, pady = 10, sticky = 's')

    def activate_button(self, user):
        self.recall_user.configure(state = 'normal')

    def load_session(self):
        user_id = self.users[self.selected_user.get()]
        self.controller.load_session(user_id)

class RecordingsFilterView(ctk.CTkFrame):

    class VariableFilter(ctk.CTkFrame):
        def __init__(self, master, variable_name: str, variable_levels: list):
            super().__init__(master)

            self.grid_columnconfigure(1, weight = 1)

            self.name = ctk.CTkLabel(master = self, text = variable_name)
            self.name.grid(column = 0, row = 0, padx = (10, 0), pady = 10, sticky = 'new')

            self.levels = []

            for index, level in enumerate(variable_levels):
                self.levels.append(ctk.CTkCheckBox(master = self, text = level))
                self.levels[-1].grid(column = index + 1, row = 0, padx = (10, 0), pady = 10, sticky = 'ne')

    def __init__(self, master, variables: dict):
        super().__init__(master)

        self.variables = []
        
        self.grid_columnconfigure(0, weight = 1)

        for index, (variable, levels) in enumerate(variables.items()):
            self.variables.append(self.VariableFilter(self, variable, levels))
            self.variables[-1].grid(column = 0, row = index + 1, padx = 10, pady = 10, sticky = 'sew')
    

class LoginView(ctk.CTkFrame):

    def submit(self):  
        day, month, year = self.birth_date.get_birthdate()
        first_name = self.first_name.get()
        last_name = self.last_name.get()
        
        self.controller.register_user(first_name = first_name, last_name = last_name, birth_day = day, birth_month = month, birth_year = year)

    def print_validation_message(self, message: str):
        self.feedback_message.configure(text = message, text_color = '#30693b')

    def print_error_message(self, message: str):
        self.feedback_message.configure(text = message, text_color = '#8d2929')

    def __init__(self, master, controller, users: dict, variables: dict):
        super().__init__(master)

        self.controller = controller
        self.users = users

        self.grid_rowconfigure([0,6], weight = 1)

        self.first_name = ctk.CTkEntry(master = self, placeholder_text = 'Prénom')
        self.first_name.grid(column = 0, row = 1, columnspan = 3, padx = 40, pady = (10,0), sticky = 'ew')

        self.last_name = ctk.CTkEntry(master = self, placeholder_text = 'Nom')
        self.last_name.grid(column = 0, row = 2, columnspan = 3, padx = 40, pady = (10,0), sticky = 'ew')

        self.birth_date = BirthDate(master = self)
        self.birth_date.grid(column = 0, row = 3, columnspan = 3, padx = 10, pady = (10,0), sticky = 'new')

        submit = ctk.CTkButton(master = self, width = 70, text = 'Valider', command = lambda: self.submit())
        submit.grid(column = 1, row = 4, padx = 0, pady = (10, 0), sticky = 'n')

        self.feedback_message = ctk.CTkLabel(master = self, text = '')
        self.feedback_message.grid(column = 0, columnspan = 3, row = 5, padx = 0, pady = (10, 0), sticky = 'new')

        self.variable_filter = RecordingsFilterView(self, variables = variables)
        self.variable_filter.grid(column = 0, columnspan = 3, row = 6, padx = 10, pady = (10,0), sticky = 'sew')

        self.load_session = LoadSessionView(master = self, controller = self.controller, users = self.users)
        self.load_session.grid(column = 0, columnspan = 3, row = 7, padx = 10, pady = 10, sticky = 'sew')