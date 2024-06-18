import customtkinter as ctk

class RatingsView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)

        self.controller = controller

        user = ctk.CTkLabel(master = self, text = 'Cool')
        user.grid_configure(row = 0, column = 0, padx = 0, pady = 0, sticky = 'new')