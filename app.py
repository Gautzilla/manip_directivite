from src.controller.app_controller import AppController

def main():
     controller = AppController()
     controller.initialize_app(initialize_db = True)

if __name__ == '__main__':
    main()