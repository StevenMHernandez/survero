"""A WorkspaceProvider Service Provider."""

from masonite.providers import Provider
from masonite.request import Request

from app.services.WorkspaceService import WorkspaceService


class WorkspaceProvider(Provider):
    """Provides Services To The Service Container."""

    # wsgi = False

    def __init__(self, application):
        self.application = application

    def register(self):
        """Register objects into the Service Container."""
        self.application.bind('app.services.WorkspaceService.WorkspaceService', WorkspaceService)

    def boot(self, request: Request):
        """Boots services required by the container."""
        pass
