from masonite.view import View
from masonite.request import Request
from masonite.controllers import Controller
from masoniteorm.query import QueryBuilder
from masonite.helpers import config

from app.services.WorkspaceService import WorkspaceService


class PublicationsController(Controller):
    def index(self, view: View, workspaceService: WorkspaceService):
        return view.render("publications.index", {'workspace': workspaceService.workspace})

    def api_index(self, workspaceService: WorkspaceService):
        papers = workspaceService.get_papers(group_by_collection_id=False)

        publications = {}
        for p in papers:
            publication_name = p['data'].get('publicationTitle', False) \
                               or p['data'].get('conferenceName', False) \
                               or p['data'].get('proceedingsTitle', False)

            if publication_name:
                if publication_name not in publications:
                    publications[publication_name] = []
                publications[publication_name].append(p)

        return {'publications': publications}
