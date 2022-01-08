from masonite.view import View
from masonite.request import Request
from masonite.controllers import Controller
from masoniteorm.query import QueryBuilder
from masonite.helpers import config

from app.services.DBAgeService import DBAgeService


class ApiController(Controller):

    def api_info(self, db_age_service: DBAgeService):
        return {
            'db_updated_at': db_age_service.updated_at_formatted(),
        }

