from model.queries import get_user_by_attributes, add_user, get_uncomplete_users as get_uncomplete_users_db
from model.models import User
from datetime import date
from model import Session

def register_user(first_name: str, last_name: str, birth_day: str, birth_month: str, birth_year: str) -> int:
    
    if len(first_name) == 0:
        raise Exception('Veuillez entrer un prénom.')
    if len(last_name) == 0:
        raise Exception('Veuillez entrer un nom.')
    try:
        birth_year, birth_month, birth_day = [int(val) for val in (birth_year, birth_month, birth_day)]
        birth_date = date(birth_year, birth_month, birth_day)
    except:
        raise Exception('Veuillez entrer une date de naissance valide.')
    
    user = User(first_name = first_name, last_name = last_name, birth_date = birth_date)

    with Session() as session:
        
        if get_user_by_attributes(user = user, session = session) is not None:
            raise Exception('Cet utilisateur a déjà été enregistré.')

        add_user(user = user, session = session)
        session.commit()

        user_id = user.id

    return user_id

def get_uncomplete_users() -> dict:
    with Session() as session:
        users = {f'{first_name} {last_name}': id for id, first_name, last_name in [(user.id, user.first_name, user.last_name) for user in get_uncomplete_users_db(session)]}
    return users
  