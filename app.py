from controller.app_controller import AppController

controller = AppController()

def main():
     controller.initialize_app(initialize_db = True)

if __name__ == '__main__':
    main()