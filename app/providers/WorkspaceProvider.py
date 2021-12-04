"""A WorkspaceProvider Service Provider."""

from masonite.provider import ServiceProvider
from masonite.request import Request

from app.services.WorkspaceService import WorkspaceService


class WorkspaceProvider(ServiceProvider):
    """Provides Services To The Service Container."""

    wsgi = False

    def register(self):
        """Register objects into the Service Container."""
        self.app.bind('app.services.WorkspaceService.WorkspaceService', WorkspaceService)

    def boot(self, request: Request):
        """Boots services required by the container."""
        pass
