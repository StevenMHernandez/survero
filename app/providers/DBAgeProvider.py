"""A WorkspaceProvider Service Provider."""

from masonite.provider import ServiceProvider
from masonite.request import Request

from app.services.DBAgeService import DBAgeService


class DBAgeProvider(ServiceProvider):
    """Provides Services To The Service Container."""

    wsgi = False

    def register(self):
        """Register objects into the Service Container."""
        self.app.bind('app.services.DBAgeService.DBAgeService', DBAgeService)

    def boot(self, db_age_service: DBAgeService):
        """Boots services required by the container."""
        pass
