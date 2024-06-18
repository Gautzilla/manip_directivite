from model.app_model import AppModel
from view.app_view import AppView

class AppController():

    def __init__(self):
        self.model = AppModel()
        self.view = AppView()

    def initialize_app(self, initialize_db : bool):

        if initialize_db:
            self.model.initialize_db()
            
        self.view.show_login()
        
        self.view.mainloop()