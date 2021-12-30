from masonite.controllers import Controller
from masonite.response import Response


class HomeController(Controller):
    def show(self, response: Response):
        return response.redirect("/")
