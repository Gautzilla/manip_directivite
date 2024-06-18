from model.login_model import register_user as register_user_model
from view.app_view import AppView

class LoginController():
    def __init__(self, app_controller, app_view: AppView):
        self.app_view = app_view
        self.app_controller = app_controller
        self.login_view = self.app_view.show_login(controller = self)

    def register_user(self, first_name: str, last_name: str, birth_day: int, birth_month: int, birth_year: int):
        try: 
            user = register_user_model(first_name = first_name, last_name = last_name, birth_day = birth_day, birth_month = birth_month, birth_year = birth_year)
        except Exception as e:
            self.login_view.print_error_message(e.args[0])
        else:
            self.login_view.print_validation_message('Utilisateur créé.')
            self.app_controller.complete_user_registration(user)