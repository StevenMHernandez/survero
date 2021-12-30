"""Verify Email Middleware."""

from masonite.request import Request
from masonite.response import Response


class VerifyEmailMiddleware:
    """Middleware To Check If The User Has Verified Their Email."""

    def before(self, request: Request, response: Response):
        """Run This Middleware Before The Route Executes."""
        user = request.user()

        if user and user.verified_at is None:
            response.redirect("/email/verify")
        return request

    def after(self, request: Request, response: Response):
        """Run This Middleware After The Route Executes."""
        return request
