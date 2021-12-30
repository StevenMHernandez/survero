"""Authentication Middleware."""

from masonite.middleware import Middleware
from masonite.request import Request
from masonite.response import Response


class AuthenticationMiddleware(Middleware):
    """Middleware To Check If The User Is Logged In."""

    def before(self, request: Request, response: Response):
        """Run This Middleware Before The Route Executes."""
        if not request.user():
            return response.redirect("/login")
        return request

    def after(self, request: Request, response: Response):
        """Run This Middleware After The Route Executes."""
        return request
