import customtkinter as ctk
from view.login_view import LoginView
from view.ratings_view import RatingsView

class AppView(ctk.CTk):

    WIDTH = 1920
    HEIGHT = 1080

    def __init__(self, controller):
        super().__init__()

        self.title('MANIP')
        self.geometry = f'{self.WIDTH}x{self.HEIGHT}'        

    def show_login(self, controller) -> LoginView:

        self.grid_columnconfigure([0,2], weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.login_view = LoginView(master = self, controller = controller)
        self.login_view.grid(column = 1, row = 0, padx = 0, pady = 0, sticky = 'nsew')

        return self.login_view
    
    def show_ratings(self, controller) -> RatingsView:
        self.ratings_view = RatingsView(master = self, controller = controller)
        self.ratings_view.grid(column = 1, row = 0, padx = 0, pady = 0, sticky = 'nsew')

        return self.ratings_view

    def close_login_view(self):
        self.login_view.grid_forget()
