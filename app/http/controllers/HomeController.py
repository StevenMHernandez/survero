from masonite.response import Response
from masonite.controllers import Controller


class HomeController(Controller):

    def index(self, response: Response):
        return response.redirect('/workspaces')
