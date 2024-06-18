from view.app_view import AppView

class RatingsController():
    def __init__(self, app_controller, app_view: AppView):
        self.app_controller = app_controller
        self.app_view = app_view

        self.app_view.show_ratings(controller = self)