import customtkinter as ctk
from src.view.login_view import LoginView
from src.view.ratings_view import RatingsView
from os import path

class AppView(ctk.CTk):

    def __init__(self, controller):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme(path.abspath(r'src/theme.json'))

        self.title('MANIP')
        self.after(0, lambda:self.state('zoomed'))        

    def show_login(self, controller, users: dict, variables: dict) -> LoginView:

        self.grid_columnconfigure([0,2], weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.login_view = LoginView(master = self, controller = controller, users = users, variables = variables)
        self.login_view.grid(column = 1, row = 0, padx = 0, pady = 0, sticky = 'nsew')

        return self.login_view
    
    def show_ratings(self, controller) -> RatingsView:
        self.ratings_view = RatingsView(master = self, controller = controller)
        self.ratings_view.grid(column = 1, row = 0, padx = 0, pady = 0, sticky = 'nsew')

        return self.ratings_view

    def close_login_view(self):
        self.login_view.grid_forget()

    def close_ratings_view(self):
        self.ratings_view.grid_forget()

    def show_test_end(self):
        self.end_message = ctk.CTkLabel(master = self, text = 'Test terminé. Merci !')
        self.end_message.grid_configure(column = 1, row = 0, padx = 10, pady = 10, sticky = 'nsew')

    def set_binding(self, sequence: str, callback: callable):
        self.bind(sequence, callback)