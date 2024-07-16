from src.model.login_model import register_user as register_user_model, get_uncomplete_users
from src.model.db_constants_filler import get_variables
from src.view.app_view import AppView

class LoginController():
    def __init__(self, app_controller, app_view: AppView):
        self.app_view = app_view
        self.app_controller = app_controller
        users = get_uncomplete_users()
        self.variables = get_variables()
        self.login_view = self.app_view.show_login(controller = self, users = users, variables = self.variables)
        self.app_view.set_binding('<Return>', lambda _ : self.login_view.submit())

    def filter_variables(self, variables: dict):
        self.variables = variables

    def load_session(self, user_id):
        self.app_controller.complete_user_registration(user_id, self.variables)

    def register_user(self, first_name: str, last_name: str, birth_day: int, birth_month: int, birth_year: int):
        try: 
            user_id = register_user_model(first_name = first_name, last_name = last_name, birth_day = birth_day, birth_month = birth_month, birth_year = birth_year)
        except Exception as e:
            self.login_view.print_error_message(e.args[0])
        else:
            self.login_view.print_validation_message('Utilisateur créé.')
            self.app_controller.complete_user_registration(user_id, self.variables)