from model.login_model import register_user as register_user_model

class LoginController():
    def __init__(self, app_controller, app_view):
        self.app_view = app_view
        self.app_controller = app_controller
        self.login_view = self.app_view.show_login(controller = self)

    def register_user(self, first_name: str, last_name: str, birth_day: int, birth_month: int, birth_year: int):
        output_text = register_user_model(first_name = first_name, last_name = last_name, birth_day = birth_day, birth_month = birth_month, birth_year = birth_year)

        if output_text == 'Utilisateur créé.':
            self.login_view.print_validation_message(output_text)
            self.app_controller.complete_user_registration()
        else:
            self.login_view.print_error_message(output_text)