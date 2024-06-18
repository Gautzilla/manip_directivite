from model.queries import get_user_by_attributes, add_user
from model.models import User
from datetime import date
from model import Session

def register_user(first_name: str, last_name: str, birth_day: int, birth_month: int, birth_year: int) -> User:
    
    if len(first_name) == 0:
        raise Exception('Veuillez entrer un prénom.')
    if len(last_name) == 0:
        raise Exception('Veuillez entrer un nom.')
    try:
        birth_date = date(birth_year, birth_month, birth_day)
    except:
        raise Exception('Veuillez entrer une date de naissance valide.')
    
    user = User(first_name = first_name, last_name = last_name, birth_date = birth_date)

    with Session() as session:
        
        if get_user_by_attributes(user = user, session = session) is not None:
            raise Exception('Cet utilisateur a déjà été enregistré.')

        add_user(user = user, session = session)

        session.commit()

    return user
        