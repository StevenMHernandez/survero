from masonite.view import View
from masonite.request import Request
from masonite.controllers import Controller


class HomeController(Controller):

    def index(self, view: View, request: Request):
        return view.render("home.index")
