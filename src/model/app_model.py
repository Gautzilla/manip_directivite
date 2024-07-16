from src.model import db_constants_filler

class AppModel():
    
    @staticmethod
    def initialize_db():
        db_constants_filler.initialize_db()