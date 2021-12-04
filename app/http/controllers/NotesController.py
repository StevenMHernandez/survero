from masonite.view import View
from masonite.request import Request
from masonite.controllers import Controller
from masoniteorm.collection import Collection
from masoniteorm.query import QueryBuilder

from app.Note import Note
from app.Workspace import Workspace
from app.services.WorkspaceService import WorkspaceService


class NotesController(Controller):
    def index(self, view: View, workspaceService: WorkspaceService):
        return view.render("notes.index", {'workspace': workspaceService.workspace})

    def create(self, request: Request):
        note = Note.create({
            'paper_key': request.input('paper_key'),
            'note': request.input('note'),
            'user_id': request.user().id,
        })
        return {"status": "success", "model": note.serialize()}

    def delete(self, request: Request):
        Note.where('id', request.param('id')).delete()
        return {"status": "success"}

    def api_index(self, workspaceService: WorkspaceService):
        notes = Collection(Note.where_in('paper_key', workspaceService.get_paper_keys()).get())
        notes.reverse()
        return notes.serialize()
