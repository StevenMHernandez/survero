from masonite.view import View
from masonite.request import Request
from masonite.controllers import Controller
from masoniteorm.collection import Collection
from masoniteorm.query import QueryBuilder

from app.Note import Note


class NotesController(Controller):

    def index(self, view: View, request: Request):
        return view.render("notes.index")

    def create(self, request: Request):
        note = Note.create({
            'paper_key': request.input('paper_key'),
            'note': request.input('note'),
            'user_id': request.user().id,
        })
        return {"status": "success", "model": note.serialize()}

    def api_index(self):
        notes = Collection(Note.all())
        notes.reverse()
        return notes.serialize()
