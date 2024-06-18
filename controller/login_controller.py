from model.login_model import register_user as register_user_model
from view.login_view import LoginView

def register_user(first_name: str, last_name: str, birth_day: int, birth_month: int, birth_year: int, login_view: LoginView):
    
    output_text = register_user_model(first_name = first_name, last_name = last_name, birth_day = birth_day, birth_month = birth_month, birth_year = birth_year)

    if output_text == 'Utilisateur créé.':
        login_view.print_validation_message(output_text)
    else:
        login_view.print_error_message(output_text)