from masonite.providers import Provider
from masonite.facades import View

from app.services.DBAgeService import DBAgeService


class DBAgeProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        self.application.bind('app.services.DBAgeService.DBAgeService', DBAgeService)

    def boot(self, db_age_service: DBAgeService):
        View.share({
            'db_updated_at': db_age_service.updated_at_formatted(),
        })
