from masonite.view import View
from masonite.request import Request
from masonite.controllers import Controller
from masoniteorm.query import QueryBuilder
from masonite.helpers import config

from app.Workspace import Workspace


class WorkspacesController(Controller):

    def index(self, view: View):
        return view.render("workspaces.index")

    def api_index(self, request: Request):
        collections = QueryBuilder().on('zotero').table('collections').order_by('parentCollectionID,collectionName').get()
        workspaces = [r['collection_key'] for r in Workspace.select('collection_key').get()]

        def add_additional_fields(r):
            r['is_workspace'] = (r['key'] in workspaces)
            return r

        collections = [add_additional_fields(r) for r in collections]
        return collections

    def create(self, request: Request):
        workspace = Workspace.create({
            'collection_key': request.input('collection_key'),
        })
        return {"status": "success", "model": workspace.serialize()}

    def delete(self, request: Request):
        Workspace.where('collection_key', request.param('workpace_key')).delete()
        return {"status": "success"}
