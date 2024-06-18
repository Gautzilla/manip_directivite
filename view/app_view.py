import customtkinter as ctk
from view.login_view import LoginView

class AppView(ctk.CTk):

    WIDTH = 1920
    HEIGHT = 1080

    def __init__(self):
        super().__init__()

        self.title('MANIP')
        self.geometry = f'{self.WIDTH}x{self.HEIGHT}'

        

    def show_login(self):

        self.grid_columnconfigure([0,2], weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        login_view = LoginView(master = self)
        login_view.grid(column = 1, row = 0, padx = 0, pady = 0, sticky = 'nsew')

    
